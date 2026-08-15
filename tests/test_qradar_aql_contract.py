import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills" / "qradar-aql"
ADAPTERS = tuple(
    ROOT / platform / "skills" / "qradar-aql"
    for platform in (".github", ".agents", ".claude")
)


class QradarAqlContractTests(unittest.TestCase):
    def test_proposal_contract_never_grants_execution(self) -> None:
        content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: qradar-aql", content)
        self.assertNotIn("allowed-tools:", content)
        for term in (
            "BLOCKED_MISSING_EVIDENCE",
            "TEMPLATE_ONLY",
            "REVIEW_REQUIRED",
            "LOCALLY_VALIDATED",
            "never means AUTHORIZED_TO_EXECUTE",
            "Never execute AQL",
            "Never put an unknown or placeholder custom property in an AQL statement",
            "security-event-analysis",
            "false-positive-analysis",
            "LOCAL_ONLY",
        ):
            self.assertIn(term, content)
        self.assertFalse((CANONICAL / "scripts").exists())

    def test_template_only_rule_keeps_placeholders_out_of_aql(self) -> None:
        guidance = (CANONICAL / "references" / "proposal-status-and-output.md").read_text(
            encoding="utf-8"
        )
        baseline = (CANONICAL / "references" / "source-and-field-baseline.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("AQL PROPOSAL is NONE", guidance)
        self.assertIn("never put a placeholder", baseline.lower())
        shared_baseline = (ROOT / "knowledge" / "qradar" / "aql-field-baseline.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("<CUSTOM_PROPERTY:", shared_baseline)
        self.assertIn("Local validation is separate from authorization to execute", shared_baseline)
        expected = json.loads(
            (ROOT / "tests" / "aql-006" / "expected.json").read_text(encoding="utf-8")
        )
        self.assertEqual("template only", expected["expected_query_behavior"])
        self.assertIn("custom-property placeholder inside AQL", expected["forbidden_behavior"])

    def test_local_validation_requires_traceable_evidence_not_authorization(self) -> None:
        expected = json.loads(
            (ROOT / "tests" / "aql-009" / "expected.json").read_text(encoding="utf-8")
        )
        self.assertEqual("locally validated read-only proposal", expected["expected_query_behavior"])
        self.assertIn("AUTHORIZED_TO_EXECUTE", expected["forbidden_behavior"])
        content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("traceable local validation evidence", content)

    def test_references_and_adapters_match(self) -> None:
        expected = {
            "source-and-field-baseline.md",
            "proposal-status-and-output.md",
            "privacy-safety-and-handoffs.md",
        }
        self.assertEqual(expected, {item.name for item in (CANONICAL / "references").glob("*.md")})
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
