import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIRED_EXPECTATION_FIELDS = {
    "expected_query_behavior",
    "expected_filters",
    "expected_time_window_behavior",
    "expected_assumptions",
    "forbidden_behavior",
}


class AqlFixtureTests(unittest.TestCase):
    def test_eight_aql_scenarios_have_complete_contracts(self) -> None:
        scenarios = sorted(ROOT.glob("aql-*"))
        self.assertGreaterEqual(len(scenarios), 8)
        for scenario in scenarios:
            with self.subTest(scenario=scenario.name):
                self.assertTrue((scenario / "input.md").is_file())
                expected = json.loads((scenario / "expected.json").read_text(encoding="utf-8"))
                self.assertTrue(REQUIRED_EXPECTATION_FIELDS.issubset(expected))
                self.assertTrue(expected["forbidden_behavior"])

    def test_skill_declares_read_only_event_boundary(self) -> None:
        skill = ROOT.parent / ".github" / "skills" / "qradar-aql" / "SKILL.md"
        self.assertTrue(skill.is_file())
        content = skill.read_text(encoding="utf-8")
        self.assertIn("name: qradar-aql", content)
        self.assertIn("FROM events", content)
        self.assertIn("Never execute AQL", content)
        self.assertIn("QUERY CANNOT BE GENERATED SAFELY", content)


if __name__ == "__main__":
    unittest.main()
