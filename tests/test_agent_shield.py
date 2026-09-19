"""Tests for Nexora Agent Shield permission and adapter auditing."""

import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.run_agent_shield import ROOT, audit


POLICY = ROOT / "standards" / "agent-shield-policy.json"


def copy_shield_fixture(destination: Path) -> None:
    for relative in (
        "framework/agents",
        ".github/agents",
        ".claude/agents",
        ".codex/agents",
        "standards/agent-shield-policy.json",
    ):
        source = ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)


class NexoraAgentShieldTests(unittest.TestCase):
    def test_repository_permission_baseline_passes(self):
        report = audit()
        self.assertEqual("PASS", report["status"])
        self.assertEqual("0.1", report["policy_version"])
        self.assertEqual(8, report["agents"])
        self.assertEqual([], report["violations"])
        self.assertEqual(8, len(report["warnings"]))

    def test_soc_execute_grant_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            copy_shield_fixture(root)
            manifest_path = root / "framework/agents/team.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            next(item for item in manifest if item["id"] == "soc-analyst")[
                "tools"
            ].append("execute")
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            report = audit(root)

        self.assertEqual("FAIL", report["status"])
        self.assertTrue(
            any("soc-analyst: manifest tools" in item for item in report["violations"])
        )

    def test_copilot_adapter_tool_escalation_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            copy_shield_fixture(root)
            adapter = root / ".github/agents/privacy-reviewer.agent.md"
            content = adapter.read_text(encoding="utf-8").replace(
                'tools: ["read", "search"]',
                'tools: ["read", "search", "execute"]',
                1,
            )
            adapter.write_text(content, encoding="utf-8")

            report = audit(root)

        self.assertEqual("FAIL", report["status"])
        self.assertTrue(
            any("privacy-reviewer: Copilot tools" in item for item in report["violations"])
        )

    def test_missing_local_only_contract_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            copy_shield_fixture(root)
            contract = root / "framework/agents/team-contract.md"
            content = contract.read_text(encoding="utf-8").replace(
                "CUSTOMER_DATA and UNKNOWN require LOCAL_ONLY",
                "Sensitive data follows an unspecified path",
                1,
            )
            contract.write_text(content, encoding="utf-8")

            report = audit(root)

        self.assertEqual("FAIL", report["status"])
        self.assertIn(
            "Shared contract missing required clause: "
            "CUSTOMER_DATA and UNKNOWN require LOCAL_ONLY",
            report["violations"],
        )


if __name__ == "__main__":
    unittest.main()
