import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills" / "false-positive-analysis"
ADAPTERS = tuple(
    ROOT / platform / "skills" / "false-positive-analysis"
    for platform in (".github", ".agents", ".claude")
)


class FalsePositiveAnalysisContractTests(unittest.TestCase):
    def test_two_axes_keep_detection_and_activity_separate(self) -> None:
        content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: false-positive-analysis", content)
        self.assertNotIn("allowed-tools:", content)
        for term in (
            "TRUE_POSITIVE",
            "FALSE_POSITIVE",
            "UNDETERMINED",
            "CONFIRMED_LEGITIMATE",
            "INCONCLUSIVE",
            "CONFIRMED_MALICIOUS",
            "Legitimate, approved, signed, or familiar activity is not by itself a false positive",
            "signed binary, known tool, maintenance period",
            "Do not execute SIEM/AQL/API/SSH actions",
            "or close tickets",
            "qradar-investigation",
            "LOCAL_ONLY",
        ):
            self.assertIn(term, content)
        metadata = (CANONICAL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("Use $false-positive-analysis", metadata)
        self.assertFalse((CANONICAL / "scripts").exists())

    def test_data_quality_fixture_preserves_uncertainty(self) -> None:
        expectation = json.loads(
            (ROOT / "tests" / "false-positive-013" / "expected.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("UNDETERMINED", expectation["expected_detection_validity"])
        self.assertEqual("INCONCLUSIVE", expectation["expected_activity_assessment"])
        self.assertIn("ticket closure", expectation["forbidden_conclusions"])

    def test_references_and_adapters_match(self) -> None:
        self.assertEqual(
            {
                "two-axis-assessment.md",
                "evidence-quality-and-thresholds.md",
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
