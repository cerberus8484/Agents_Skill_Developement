import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills" / "security-event-analysis"
ADAPTERS = tuple(
    ROOT / platform / "skills" / "security-event-analysis"
    for platform in (".github", ".agents", ".claude")
)


class SecurityEventAnalysisContractTests(unittest.TestCase):
    def test_evidence_producer_contract_is_bounded(self) -> None:
        content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: security-event-analysis", content)
        self.assertNotIn("allowed-tools:", content)
        for term in (
            "untrusted data",
            "never correct, redact, normalize over, or silently replace raw content",
            "device/event time, SIEM receive time, SIEM stored/start time",
            "never causal proof",
            "must remain UNASSESSED, UNKNOWN, or INCONCLUSIVE",
            "Never execute SIEM/AQL/API/SSH actions",
            "qradar-investigation",
            "false-positive-analysis",
            "LOCAL_ONLY",
        ):
            self.assertIn(term, content)
        metadata = (CANONICAL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("Use $security-event-analysis", metadata)
        self.assertFalse((CANONICAL / "scripts").exists())

    def test_provenance_and_time_references_define_the_boundaries(self) -> None:
        provenance = (CANONICAL / "references" / "provenance-and-evidence.md").read_text(
            encoding="utf-8"
        )
        time = (CANONICAL / "references" / "time-and-correlation.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Do not overwrite raw data", provenance)
        self.assertIn("None of these labels proves causation", time)
        expectation = json.loads(
            (ROOT / "tests" / "event-analysis-011" / "expected.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("causation is established", expectation["forbidden_conclusions"])

    def test_references_and_adapters_match(self) -> None:
        self.assertEqual(
            {
                "provenance-and-evidence.md",
                "time-and-correlation.md",
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
