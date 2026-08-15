"""Generate GitHub Copilot skill adapters from canonical framework skills."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills"
COPILOT = ROOT / ".github" / "skills"
SKILLS = ("clean-code",)


def sync_skill(name: str) -> None:
    source = CANONICAL / name
    destination = COPILOT / name
    if not (source / "SKILL.md").is_file():
        raise FileNotFoundError(f"Missing canonical SKILL.md for {name}")
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def main() -> None:
    for skill in SKILLS:
        sync_skill(skill)


if __name__ == "__main__":
    main()
