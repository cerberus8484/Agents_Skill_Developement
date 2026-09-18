"""Synchronize canonical Nexora Skills into platform adapter directories.

The default mode writes only expected files. It never deletes unexpected files.
Use --check in CI to detect drift and --prune only for an explicit cleanup.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills"
ADAPTERS = (
    ROOT / ".github" / "skills",
    ROOT / ".agents" / "skills",
    ROOT / ".claude" / "skills",
)
VALID_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def discover_skills() -> tuple[str, ...]:
    """Return validated canonical skill names in deterministic order."""
    skills = []
    for path in sorted(CANONICAL.iterdir()):
        if not path.is_dir():
            continue
        if path.is_symlink():
            raise ValueError(f"Canonical skill must not be a symlink: {path}")
        if not VALID_NAME.fullmatch(path.name):
            raise ValueError(f"Invalid skill name: {path.name!r}")
        if not (path / "SKILL.md").is_file():
            raise FileNotFoundError(f"Missing canonical SKILL.md for {path.name}")
        skills.append(path.name)
    if not skills:
        raise RuntimeError("No canonical skills found")
    return tuple(skills)


def render_all() -> dict[Path, bytes]:
    """Return every deterministic repository-relative adapter output."""
    outputs: dict[Path, bytes] = {}
    for name in discover_skills():
        source_root = CANONICAL / name
        for source in sorted(source_root.rglob("*")):
            if source.is_symlink():
                raise ValueError(f"Canonical skill content must not be a symlink: {source}")
            if not source.is_file():
                continue
            relative = source.relative_to(source_root)
            content = source.read_bytes()
            for adapter_root in ADAPTERS:
                destination = adapter_root / name / relative
                repository_relative = destination.relative_to(ROOT)
                if repository_relative in outputs:
                    raise ValueError(f"Duplicate adapter output: {repository_relative}")
                outputs[repository_relative] = content
    return outputs


def find_drift(outputs: dict[Path, bytes]) -> list[str]:
    """Report missing, changed, and unexpected generated adapter files."""
    drift = []
    expected = set(outputs)
    for relative, content in outputs.items():
        path = ROOT / relative
        if not path.is_file():
            drift.append(f"MISSING {relative}")
        elif path.is_symlink():
            drift.append(f"SYMLINK {relative}")
        elif path.read_bytes() != content:
            drift.append(f"CHANGED {relative}")

    generated_skill_names = {relative.parts[2] for relative in expected}
    for adapter_root in ADAPTERS:
        for name in sorted(generated_skill_names):
            generated_root = adapter_root / name
            if not generated_root.exists():
                continue
            for path in sorted(generated_root.rglob("*")):
                if path.is_file() or path.is_symlink():
                    relative = path.relative_to(ROOT)
                    if relative not in expected:
                        drift.append(f"UNEXPECTED {relative}")
    return drift


def write_outputs(outputs: dict[Path, bytes]) -> None:
    """Write expected files without deleting unrelated or unexpected content."""
    for relative, content in outputs.items():
        path = ROOT / relative
        if path.exists() and path.is_symlink():
            raise ValueError(f"Refusing to replace symlink: {relative}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def prune_unexpected(outputs: dict[Path, bytes]) -> None:
    """Delete only files inside adapter roots that are absent from canonical output."""
    expected = set(outputs)
    generated_skill_names = {relative.parts[2] for relative in expected}
    for adapter_root in ADAPTERS:
        if not adapter_root.exists() or adapter_root.is_symlink():
            continue
        for name in sorted(generated_skill_names):
            generated_root = adapter_root / name
            if not generated_root.exists():
                continue
            for path in sorted(generated_root.rglob("*"), reverse=True):
                relative = path.relative_to(ROOT)
                if path.is_symlink():
                    raise ValueError(f"Refusing to prune symlink: {relative}")
                if path.is_file() and relative not in expected:
                    path.unlink()
                elif path.is_dir() and not any(path.iterdir()):
                    path.rmdir()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Detect drift without writes.")
    mode.add_argument(
        "--prune",
        action="store_true",
        help="Synchronize and explicitly remove unexpected adapter files.",
    )
    args = parser.parse_args()

    outputs = render_all()
    if args.check:
        drift = find_drift(outputs)
        if drift:
            parser.exit(1, "Adapter drift:\n" + "\n".join(drift) + "\n")
        print(f"{len(outputs)} adapter files checked; no differences.")
        return

    write_outputs(outputs)
    if args.prune:
        prune_unexpected(outputs)
    remaining = find_drift(outputs)
    if remaining:
        print("Expected adapter files synchronized; unresolved drift:")
        print("\n".join(remaining))
    else:
        print(f"{len(outputs)} adapter files synchronized.")


if __name__ == "__main__":
    main()
