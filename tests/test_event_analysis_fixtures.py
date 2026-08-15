import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIRED_EXPECTATION_FIELDS = {
    "expected_facts",
    "expected_observations",
    "expected_data_quality_issues",
    "expected_findings",
    "expected_evidence_id_behavior",
    "forbidden_conclusions",
}


class EventAnalysisFixtureTests(unittest.TestCase):
    def test_ten_event_analysis_scenarios_have_complete_contracts(self) -> None:
        scenarios = sorted(ROOT.glob("event-analysis-*"))
        self.assertGreaterEqual(len(scenarios), 10)
        for scenario in scenarios:
            with self.subTest(scenario=scenario.name):
                self.assertTrue((scenario / "input.md").is_file())
                expected = json.loads((scenario / "expected.json").read_text(encoding="utf-8"))
                self.assertTrue(REQUIRED_EXPECTATION_FIELDS.issubset(expected))
                self.assertTrue(expected["expected_evidence_id_behavior"])
                self.assertTrue(expected["forbidden_conclusions"])

    def test_skill_declares_evidence_producer_boundary(self) -> None:
        skill = ROOT.parent / ".github" / "skills" / "security-event-analysis" / "SKILL.md"
        self.assertTrue(skill.is_file())
        content = skill.read_text(encoding="utf-8")
        self.assertIn("name: security-event-analysis", content)
        self.assertIn("Never execute SIEM/AQL/API/SSH actions", content)
        self.assertIn("RETURN TO INVESTIGATION", content)


if __name__ == "__main__":
    unittest.main()
