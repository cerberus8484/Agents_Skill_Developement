"""Cross-platform contract checks for the SOC benchmark mode."""

import json
import tomllib
import unittest
from pathlib import Path

from tools.sync_agents import ROOT, render_all


ROLE = ROOT / "framework" / "agents" / "soc-analyst.md"
STANDARD = ROOT / "standards" / "benchmark-decision-standard.md"
RESPONSE_SCHEMA = ROOT / "benchmarks" / "schemas" / "agent-benchmark-response.schema.json"
SOC_OUTPUTS = {
    Path(".github/agents/soc-analyst.agent.md"),
    Path(".claude/agents/soc-analyst.md"),
    Path(".codex/agents/soc-analyst.toml"),
}


class SocBenchmarkAgentContractTests(unittest.TestCase):
    def test_benchmark_mode_is_explicit_and_does_not_replace_normal_output(self):
        content = ROLE.read_text(encoding="utf-8")
        for clause in (
            "Enter benchmark mode only",
            "NAB-[0-9]{3}",
            "untrusted evidence",
            "Return one JSON object",
            "NOT_RUN",
            "Outside an explicit NAB case",
        ):
            self.assertIn(clause, content)

    def test_decision_standard_matches_response_schema_enum(self):
        standard = STANDARD.read_text(encoding="utf-8")
        schema = json.loads(RESPONSE_SCHEMA.read_text(encoding="utf-8"))
        decisions = schema["properties"]["decisions"]["items"]["enum"]
        self.assertEqual(9, len(decisions))
        for decision in decisions:
            with self.subTest(decision=decision):
                self.assertIn(f"`{decision}`", standard)

    def test_all_soc_platform_adapters_preserve_benchmark_contract(self):
        outputs = render_all()
        self.assertTrue(SOC_OUTPUTS.issubset(outputs))
        for path in SOC_OUTPUTS:
            content = outputs[path]
            if path.suffix == ".toml":
                content = tomllib.loads(content)["developer_instructions"]
            for clause in (
                "## Nexora Agent Bench mode",
                "benchmark-response.schema.json",
                "benchmark-decision-standard.md",
                "do not force benchmark JSON",
            ):
                with self.subTest(path=path, clause=clause):
                    self.assertIn(clause, content)


if __name__ == "__main__":
    unittest.main()
