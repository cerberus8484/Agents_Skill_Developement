import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIRED_EXPECTATION_FIELDS = {
    "expected_facts",
    "expected_missing_evidence",
    "expected_investigation_steps",
    "expected_query",
    "forbidden_conclusions",
    "expected_assessment",
}


class TriageFixtureTests(unittest.TestCase):
    def test_schemas_are_valid_json_documents(self) -> None:
        schema_directory = ROOT.parent / "schemas"
        schema_files = sorted(schema_directory.glob("*.schema.json"))
        self.assertEqual(4, len(schema_files))

        for schema_file in schema_files:
            with self.subTest(schema=schema_file.name):
                schema = json.loads(schema_file.read_text(encoding="utf-8"))
                self.assertEqual("object", schema["type"])
                self.assertIn("required", schema)

    def test_each_ticket_has_a_complete_contract(self) -> None:
        ticket_directories = sorted(ROOT.glob("ticket-*"))
        self.assertGreaterEqual(len(ticket_directories), 3)

        for ticket_directory in ticket_directories:
            with self.subTest(ticket=ticket_directory.name):
                input_file = ticket_directory / "input.md"
                expected_file = ticket_directory / "expected.json"
                self.assertTrue(input_file.is_file(), "missing synthetic input")
                self.assertTrue(expected_file.is_file(), "missing expected contract")

                expected = json.loads(expected_file.read_text(encoding="utf-8"))
                self.assertTrue(REQUIRED_EXPECTATION_FIELDS.issubset(expected))
                self.assertTrue(expected["expected_facts"])
                self.assertTrue(expected["expected_missing_evidence"])
                self.assertTrue(expected["expected_investigation_steps"])
                self.assertTrue(expected["forbidden_conclusions"])
                self.assertIn(expected["expected_assessment"]["classification"], {
                    "UNASSESSED", "UNKNOWN", "SUSPICIOUS", "LIKELY_LEGITIMATE",
                    "CONFIRMED_LEGITIMATE", "CONFIRMED_MALICIOUS",
                })
                self.assertIn(expected["expected_assessment"]["confidence"], {"LOW", "MEDIUM", "HIGH"})

    def test_skill_and_tests_are_present(self) -> None:
        skill = ROOT.parent / ".github" / "skills" / "siem-ticket-triage" / "SKILL.md"
        self.assertTrue(skill.is_file())
        content = skill.read_text(encoding="utf-8")
        self.assertIn("name: siem-ticket-triage", content)
        self.assertIn("Never use it for production access", content)


if __name__ == "__main__":
    unittest.main()
