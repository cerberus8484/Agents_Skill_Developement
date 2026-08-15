import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills" / "siem-ticket-triage"
ADAPTERS = tuple(
    ROOT / platform / "skills" / "siem-ticket-triage"
    for platform in (".github", ".agents", ".claude")
)


class SiemTicketTriageContractTests(unittest.TestCase):
    def test_contract_has_safe_triage_boundaries(self) -> None:
        content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: siem-ticket-triage", content)
        self.assertNotIn("allowed-tools:", content)
        for term in (
            "untrusted data",
            "Create E001",
            "Do not execute or write AQL",
            "security-event-analysis",
            "false-positive-analysis",
            "incident-summary",
            "LOCAL_ONLY",
            "not decide what happened",
        ):
            self.assertIn(term, content)
        metadata = (CANONICAL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("Use $siem-ticket-triage", metadata)
        self.assertFalse((CANONICAL / "scripts").exists())

    def test_references_and_adapters_match(self) -> None:
        expected = {
            "scope-and-evidence.md",
            "state-and-handoff.md",
            "privacy-and-safety.md",
        }
        self.assertEqual(
            expected,
            {item.name for item in (CANONICAL / "references").glob("*.md")},
        )
        source_files = {
            item.relative_to(CANONICAL)
            for item in CANONICAL.rglob("*")
            if item.is_file()
        }
        for adapter in ADAPTERS:
            target_files = {
                item.relative_to(adapter)
                for item in adapter.rglob("*")
                if item.is_file()
            }
            self.assertEqual(source_files, target_files)
            for path in source_files:
                self.assertEqual(
                    (CANONICAL / path).read_bytes(),
                    (adapter / path).read_bytes(),
                )

    def test_existing_synthetic_cases_still_require_conservative_triage(self) -> None:
        expectations = [
            json.loads((ROOT / "tests" / ticket / "expected.json").read_text(encoding="utf-8"))
            for ticket in ("ticket-001", "ticket-002", "ticket-003")
        ]
        self.assertEqual(
            ["SUSPICIOUS", "UNASSESSED", "SUSPICIOUS"],
            [case["expected_assessment"]["classification"] for case in expectations],
        )
        for case in expectations:
            self.assertEqual("LOW", case["expected_assessment"]["confidence"])
            self.assertTrue(case["forbidden_conclusions"])


if __name__ == "__main__":
    unittest.main()
