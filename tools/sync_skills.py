"""Generate cross-platform skill adapters from canonical framework skills."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills"
ADAPTERS = (
    ROOT / ".github" / "skills",
    ROOT / ".agents" / "skills",
    ROOT / ".claude" / "skills",
)
SKILLS = (
    "clean-code",
    "security",
    "dsgvo",
    "design-system",
    "soc-forensic-hunts",
    "siem-ticket-triage",
    "qradar-investigation",
    "qradar-aql",
    "security-event-analysis",
)


def sync_skill(name: str) -> None:
    source = CANONICAL / name
    if not (source / "SKILL.md").is_file():
        raise FileNotFoundError(f"Missing canonical SKILL.md for {name}")
    for adapter_root in ADAPTERS:
        destination = adapter_root / name
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)


def main() -> None:
    for skill in SKILLS:
        sync_skill(skill)


if __name__ == "__main__":
    main()
