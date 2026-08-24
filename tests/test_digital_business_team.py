"""Contract checks for the local Codex Digital Business Team."""

from __future__ import annotations

import tomllib
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
AGENT_DIRECTORY = REPOSITORY_ROOT / ".codex" / "agents"
TEAM_MANIFEST = REPOSITORY_ROOT / "framework" / "teams" / "digital-business-team.md"

ROLES = (
    "digital-business-team-lead",
    "website-ux-agent",
    "seo-agent",
    "marketing-growth-agent",
    "copywriter-content-agent",
    "brand-design-agent",
    "analytics-agent",
    "quality-review-agent",
)


class DigitalBusinessTeamContractTests(unittest.TestCase):
    def test_manifest_declares_all_local_roles_and_boundaries(self) -> None:
        manifest = TEAM_MANIFEST.read_text(encoding="utf-8")

        for role in ROLES:
            self.assertIn(f"`{role}`", manifest)

        self.assertIn("separate from the SIEM team", manifest)
        self.assertIn("no Notion", manifest)
        self.assertIn("No agent publishes, spends money, contacts people", manifest)
        self.assertIn("CUSTOMER_DATA and UNKNOWN are LOCAL_ONLY", manifest)

    def test_each_codex_adapter_has_its_matching_name_and_local_boundary(self) -> None:
        for role in ROLES:
            with self.subTest(role=role):
                adapter = tomllib.loads(
                    (AGENT_DIRECTORY / f"{role}.toml").read_text(encoding="utf-8")
                )
                instructions = adapter["developer_instructions"]

                self.assertEqual(adapter["name"], role)
                self.assertIn("LOCAL_ONLY", instructions)
                self.assertIn("Do not", instructions)

    def test_priority_and_external_action_boundaries_are_explicit(self) -> None:
        lead = tomllib.loads(
            (AGENT_DIRECTORY / "digital-business-team-lead.toml").read_text(
                encoding="utf-8"
            )
        )["developer_instructions"]
        quality = tomllib.loads(
            (AGENT_DIRECTORY / "quality-review-agent.toml").read_text(encoding="utf-8")
        )["developer_instructions"]

        self.assertIn("You alone may change team priorities", lead)
        self.assertIn("publish content", lead)
        self.assertIn("PASS", quality)
        self.assertIn("approve publication", quality)


if __name__ == "__main__":
    unittest.main()
