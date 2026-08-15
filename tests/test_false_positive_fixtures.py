import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIRED = {"expected_detection_validity", "expected_activity_assessment", "expected_support", "expected_contradictions", "expected_missing_evidence", "forbidden_conclusions"}


class FalsePositiveFixtureTests(unittest.TestCase):
    def test_twelve_assessment_scenarios_have_complete_contracts(self) -> None:
        scenarios = sorted(ROOT.glob("false-positive-*"))
        self.assertGreaterEqual(len(scenarios), 12)
        for scenario in scenarios:
            with self.subTest(scenario=scenario.name):
                self.assertTrue((scenario / "input.md").is_file())
                expected = json.loads((scenario / "expected.json").read_text(encoding="utf-8"))
                self.assertTrue(REQUIRED.issubset(expected))
                self.assertTrue(expected["forbidden_conclusions"])

    def test_skill_declares_two_axis_and_no_close_boundary(self) -> None:
        skill = ROOT.parent / ".github" / "skills" / "false-positive-analysis" / "SKILL.md"
        content = skill.read_text(encoding="utf-8")
        self.assertIn("name: false-positive-analysis", content)
        self.assertIn("DETECTION VALIDITY", content)
        self.assertIn("ACTIVITY ASSESSMENT", content)
        self.assertIn("Never execute a query", content)


if __name__ == "__main__":
    unittest.main()
