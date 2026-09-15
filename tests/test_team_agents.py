"""Structural checks, not model-behavior or runtime validation."""

import json
import tomllib
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from tools import sync_agents
from tools.sync_agents import ROOT, render_all


class TeamAgentTests(unittest.TestCase):
    def test_generated_adapters_match_sources(self):
        outputs = render_all()
        self.assertEqual(24, len(outputs))
        for path, expected in outputs.items():
            with self.subTest(path=path):
                self.assertEqual(expected, (ROOT / path).read_text(encoding="utf-8"))

    def test_shared_contract_and_role_survive_all_adapters(self):
        for path, content in render_all().items():
            if path.suffix == ".toml":
                content = tomllib.loads(content)["developer_instructions"]
            for clause in ("LOCAL_ONLY", "untrusted", "UNTESTED", "## Workflow",
                           "## Acceptance", "## Output", "## Stop and recovery"):
                with self.subTest(path=path, clause=clause):
                    self.assertIn(clause, content)

    def test_tools_and_skill_references(self):
        profiles = json.loads((ROOT / "framework/agents/team.json").read_text())
        for profile in profiles:
            for skill in profile["skills"]:
                for folder in (".github", ".agents", ".claude"):
                    self.assertTrue((ROOT / folder / "skills" / skill / "SKILL.md").is_file())
            if profile["id"] in ("soc-analyst", "privacy-reviewer", "code-security-reviewer"):
                self.assertEqual(["read", "search"], profile["tools"])
            self.assertNotIn("*", profile["tools"])
            self.assertEqual(profile["id"] == "team-lead", "agent" in profile["tools"])

    def test_codex_roundtrip_keeps_exact_canonical_contract(self):
        shared = (ROOT / "framework/agents/team-contract.md").read_text(encoding="utf-8")
        for path, content in render_all().items():
            if path.suffix == ".toml":
                data = tomllib.loads(content)
                role = (ROOT / "framework/agents" / f"{data['name']}.md").read_text(
                    encoding="utf-8"
                )
                self.assertEqual(shared + "\n" + role, data["developer_instructions"])

    def test_sync_and_check_do_not_touch_unregistered_files(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            sentinel = root / "unrelated.txt"
            sentinel.write_text("preserve", encoding="utf-8")
            outputs = {Path(".github/agents/test.agent.md"): "synthetic\n"}
            with patch.object(sync_agents, "ROOT", root), patch.object(
                sync_agents, "render_all", return_value=outputs
            ), redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                with patch("sys.argv", ["sync_agents.py", "--check"]):
                    with self.assertRaises(SystemExit) as missing:
                        sync_agents.main()
                    self.assertEqual(1, missing.exception.code)
                    self.assertFalse((root / ".github").exists())
                with patch("sys.argv", ["sync_agents.py"]):
                    sync_agents.main()
                    sync_agents.main()
                with patch("sys.argv", ["sync_agents.py", "--check"]):
                    sync_agents.main()
                    target = root / next(iter(outputs))
                    target.write_text("drift", encoding="utf-8")
                    with self.assertRaises(SystemExit) as drift:
                        sync_agents.main()
                    self.assertEqual(1, drift.exception.code)
                    self.assertEqual("drift", target.read_text(encoding="utf-8"))
            self.assertEqual("preserve", sentinel.read_text(encoding="utf-8"))

    def test_invalid_ids_and_duplicate_profiles_fail_before_writes(self):
        profiles = json.loads((ROOT / "framework/agents/team.json").read_text())
        for invalid in ("../escape", "", "UpperCase"):
            with patch.object(sync_agents.json, "loads", return_value=[
                {**profiles[0], "id": invalid}
            ]):
                with self.assertRaisesRegex(ValueError, "Invalid agent ID"):
                    render_all()
        with patch.object(sync_agents.json, "loads", return_value=[profiles[0], profiles[0]]):
            with self.assertRaisesRegex(ValueError, "Duplicate agent output"):
                render_all()


if __name__ == "__main__":
    unittest.main()
