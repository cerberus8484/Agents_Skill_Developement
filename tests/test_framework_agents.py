import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
AGENTS = ("privacy-reviewer", "security-fixer", "dsgvo-fixer")


class FrameworkAgentTests(unittest.TestCase):
    def test_canonical_roles_have_all_platform_adapters(self) -> None:
        for agent in AGENTS:
            with self.subTest(agent=agent):
                canonical = (ROOT / "framework" / "agents" / f"{agent}.md").read_text(
                    encoding="utf-8"
                )
                copilot = (ROOT / ".github" / "agents" / f"{agent}.agent.md").read_text(
                    encoding="utf-8"
                )
                claude = (ROOT / ".claude" / "agents" / f"{agent}.md").read_text(
                    encoding="utf-8"
                )
                codex = tomllib.loads(
                    (ROOT / ".codex" / "agents" / f"{agent}.toml").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertIn(f"`{agent}`", canonical)
                self.assertIn("STRUCTURAL_ONLY", canonical)
                self.assertIn("user-invocable: true", copilot)
                self.assertIn(f"name: {agent}", claude)
                self.assertEqual(agent, codex["name"])
                self.assertTrue(codex["developer_instructions"])

    def test_roles_keep_review_and_execution_boundaries(self) -> None:
        privacy = (ROOT / ".codex" / "agents" / "privacy-reviewer.toml").read_text(
            encoding="utf-8"
        )
        security_fixer = (ROOT / ".codex" / "agents" / "security-fixer.toml").read_text(
            encoding="utf-8"
        )
        dsgvo_fixer = (ROOT / ".codex" / "agents" / "dsgvo-fixer.toml").read_text(
            encoding="utf-8"
        )
        self.assertIn("Do not provide legal advice", privacy)
        self.assertIn("LOCAL_ONLY", privacy)
        self.assertIn("explicitly approved finding", security_fixer)
        self.assertIn("Do not scan external targets", security_fixer)
        self.assertIn("explicitly approved technical privacy requirement", dsgvo_fixer)
        self.assertIn("Do not execute production deletion", dsgvo_fixer)


if __name__ == "__main__":
    unittest.main()
