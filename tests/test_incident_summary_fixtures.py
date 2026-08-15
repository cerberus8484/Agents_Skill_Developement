import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIRED = {"expected_mode", "expected_traceability", "expected_consistency", "expected_assessment_behavior", "forbidden_conclusions"}


class IncidentSummaryFixtureTests(unittest.TestCase):
    def test_twelve_summary_scenarios_have_complete_contracts(self) -> None:
        scenarios = sorted(ROOT.glob("incident-summary-*"))
        self.assertGreaterEqual(len(scenarios), 12)
        for scenario in scenarios:
            with self.subTest(scenario=scenario.name):
                self.assertTrue((scenario / "input.md").is_file())
                expected = json.loads((scenario / "expected.json").read_text(encoding="utf-8"))
                self.assertTrue(REQUIRED.issubset(expected))
                self.assertTrue(expected["forbidden_conclusions"])

    def test_skill_is_reporting_only(self) -> None:
        skill = ROOT.parent / ".github" / "skills" / "incident-summary" / "SKILL.md"
        content = skill.read_text(encoding="utf-8")
        self.assertIn("name: incident-summary", content)
        self.assertIn("SUMMARY CONSISTENCY WARNING", content)
        self.assertIn("Never execute a query", content)


if __name__ == "__main__":
    unittest.main()
