import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills" / "incident-summary"
ADAPTERS = tuple(
    ROOT / platform / "skills" / "incident-summary"
    for platform in (".github", ".agents", ".claude")
)


class IncidentSummaryContractTests(unittest.TestCase):
    def test_reporting_contract_is_faithful_and_non_operational(self) -> None:
        content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: incident-summary", content)
        self.assertNotIn("allowed-tools:", content)
        self.assertIn("standards/data-handling-standard.md", content)
        for term in (
            "untrusted data",
            "final presentation of the supplied investigation packet",
            "SUMMARY CONSISTENCY WARNING",
            "Do not normalize, parse, correlate, enrich, reconcile",
            "Preserve `TRUE_POSITIVE`",
            "Never silently select an authoritative representation",
            "Never execute a query",
            "or close tickets",
            "qradar-investigation",
            "security-event-analysis",
            "false-positive-analysis",
            "LOCAL_ONLY",
        ):
            self.assertIn(term, content)
        metadata = (CANONICAL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("Use $incident-summary", metadata)
        self.assertFalse((CANONICAL / "scripts").exists())

    def test_completed_state_with_gap_requires_a_warning(self) -> None:
        expectation = json.loads(
            (ROOT / "tests" / "incident-summary-013" / "expected.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("FINAL INVESTIGATION SUMMARY", expectation["expected_mode"])
        self.assertTrue(expectation["expected_consistency"])
        self.assertIn("ticket can be closed", expectation["forbidden_conclusions"])

    def test_references_and_adapters_match(self) -> None:
        self.assertEqual(
            {
                "reporting-contract.md",
                "traceability-and-consistency.md",
                "privacy-safety-and-handoffs.md",
            },
            {item.name for item in (CANONICAL / "references").glob("*.md")},
        )
        source_files = {
            item.relative_to(CANONICAL)
            for item in CANONICAL.rglob("*")
            if item.is_file()
        }
        for adapter in ADAPTERS:
            adapter_files = {
                item.relative_to(adapter)
                for item in adapter.rglob("*")
                if item.is_file()
            }
            self.assertEqual(source_files, adapter_files)
            for path in source_files:
                self.assertEqual(
                    (CANONICAL / path).read_bytes(),
                    (adapter / path).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
