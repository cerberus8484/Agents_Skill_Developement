import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills" / "qradar-investigation"
ADAPTERS = tuple(
    ROOT / platform / "skills" / "qradar-investigation"
    for platform in (".github", ".agents", ".claude")
)


class QradarInvestigationContractTests(unittest.TestCase):
    def test_orchestration_contract_is_bounded(self) -> None:
        content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: qradar-investigation", content)
        self.assertNotIn("allowed-tools:", content)
        for term in (
            "untrusted data",
            "not decide what happened",
            "single evidence-supported proposed next investigation step",
            "not proof that it is the globally optimal action",
            "Do not execute or write AQL",
            "security-event-analysis",
            "false-positive-analysis",
            "incident-summary",
            "LOCAL_ONLY",
            "authorized human",
        ):
            self.assertIn(term, content)
        metadata = (CANONICAL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("Use $qradar-investigation", metadata)
        self.assertFalse((CANONICAL / "scripts").exists())

    def test_references_and_adapters_match(self) -> None:
        self.assertEqual(
            {
                "scope-and-evidence.md",
                "orchestration-and-handoffs.md",
                "privacy-and-safety.md",
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

    def test_existing_synthetic_cases_remain_conservative(self) -> None:
        expectations = [
            json.loads((ROOT / "tests" / f"investigation-{number:03d}" / "expected.json").read_text(encoding="utf-8"))
            for number in range(1, 6)
        ]
        self.assertEqual(
            ["UNKNOWN", "UNKNOWN", "SUSPICIOUS", "UNKNOWN", "UNKNOWN"],
            [case["expected_assessment"]["classification"] for case in expectations],
        )
        self.assertTrue(all(case["forbidden_conclusions"] for case in expectations))
        self.assertEqual(
            ["LOW", "LOW", "LOW", "LOW", "LOW"],
            [case["expected_assessment"]["confidence"] for case in expectations],
        )


if __name__ == "__main__":
    unittest.main()
