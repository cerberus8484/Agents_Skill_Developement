"""Install Nexora skills and agents for the current Codex user safely.

The installer owns only the named Nexora packages. Existing packages with the
same names are moved to a timestamped backup before complete directory/file
replacement. Unrelated personal skills and agents are never removed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import sync_agents, sync_skills


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def validate_sources() -> tuple[tuple[str, ...], tuple[str, ...]]:
    skill_outputs = sync_skills.render_all()
    skill_drift = sync_skills.find_drift(skill_outputs)
    if skill_drift:
        raise RuntimeError("Generated skill adapters have drift; run tools/sync_skills.py --prune")

    agent_outputs = sync_agents.render_all()
    agent_drift = [
        str(relative)
        for relative, content in agent_outputs.items()
        if not (ROOT / relative).is_file()
        or (ROOT / relative).read_text(encoding="utf-8") != content
    ]
    if agent_drift:
        raise RuntimeError("Generated agent adapters have drift; run tools/sync_agents.py")

    return sync_skills.discover_skills(), tuple(
        sorted(path.stem for path in (ROOT / ".codex" / "agents").glob("*.toml"))
    )


def replace_path(source: Path, destination: Path, backup: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    backup.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as staging_directory:
        staged = Path(staging_directory) / destination.name
        if source.is_dir():
            shutil.copytree(source, staged)
        else:
            shutil.copy2(source, staged)
        if destination.exists() or destination.is_symlink():
            if destination.is_symlink():
                raise RuntimeError(f"Refusing to replace symlink: {destination}")
            if backup.exists():
                raise RuntimeError(f"Backup collision: {backup}")
            shutil.move(str(destination), str(backup))
        os.replace(staged, destination)


def install(home: Path, *, dry_run: bool = False) -> dict[str, object]:
    skills, agents = validate_sources()
    user_skills = home / ".agents" / "skills"
    user_agents = home / ".codex" / "agents"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = home / ".nexora" / "backups" / f"codex-{timestamp}"

    operations = []
    for name in skills:
        operations.append((ROOT / ".agents" / "skills" / name, user_skills / name, backup_root / "skills" / name))
    for name in agents:
        operations.append((ROOT / ".codex" / "agents" / f"{name}.toml", user_agents / f"{name}.toml", backup_root / "agents" / f"{name}.toml"))

    if not dry_run:
        for source, destination, backup in operations:
            replace_path(source, destination, backup)

    files = []
    for _, destination, _ in operations:
        if dry_run:
            continue
        paths = [destination] if destination.is_file() else sorted(path for path in destination.rglob("*") if path.is_file())
        files.extend({"path": str(path), "sha256": sha256(path)} for path in paths)

    manifest = {
        "status": "DRY_RUN" if dry_run else "INSTALLED",
        "skills": list(skills),
        "agents": list(agents),
        "backup": str(backup_root),
        "files": files,
        "restart_required": True,
    }
    if not dry_run:
        backup_root.mkdir(parents=True, exist_ok=True)
        (backup_root / "install-manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home(), help="Target user home directory.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and show the plan without writing.")
    args = parser.parse_args()
    result = install(args.home.resolve(), dry_run=args.dry_run)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not args.dry_run:
        print("Restart Codex completely before testing newly installed agent types.")


if __name__ == "__main__":
    main()
