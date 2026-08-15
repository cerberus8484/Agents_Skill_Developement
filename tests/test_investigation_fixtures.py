import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIRED_EXPECTATION_FIELDS = {
    "expected_facts",
    "expected_observations_or_inferences",
    "expected_hypotheses",
    "expected_missing_evidence",
    "expected_next_step",
    "expected_query_request",
    "forbidden_conclusions",
    "expected_assessment",
}


class InvestigationFixtureTests(unittest.TestCase):
    def test_five_investigation_scenarios_have_complete_contracts(self) -> None:
        scenarios = sorted(ROOT.glob("investigation-*"))
        self.assertGreaterEqual(len(scenarios), 5)

        for scenario in scenarios:
            with self.subTest(scenario=scenario.name):
                input_file = scenario / "input.md"
                expected_file = scenario / "expected.json"
                self.assertTrue(input_file.is_file(), "missing synthetic input")
                self.assertTrue(expected_file.is_file(), "missing expected contract")
                expected = json.loads(expected_file.read_text(encoding="utf-8"))
                self.assertTrue(REQUIRED_EXPECTATION_FIELDS.issubset(expected))
                self.assertTrue(expected["expected_hypotheses"])
                self.assertTrue(expected["expected_missing_evidence"])
                self.assertTrue(expected["expected_next_step"])
                self.assertTrue(expected["forbidden_conclusions"])
                self.assertIn(expected["expected_assessment"]["confidence"], {"LOW", "MEDIUM", "HIGH"})

    def test_skill_declares_safe_orchestration_boundary(self) -> None:
        skill = ROOT.parent / ".github" / "skills" / "qradar-investigation" / "SKILL.md"
        self.assertTrue(skill.is_file())
        content = skill.read_text(encoding="utf-8")
        self.assertIn("name: qradar-investigation", content)
        self.assertIn("Never execute", content)
        self.assertIn("QUERY REQUEST", content)


if __name__ == "__main__":
    unittest.main()
