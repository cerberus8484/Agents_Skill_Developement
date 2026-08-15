import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills" / "soc-forensic-hunts"
ADAPTERS = tuple(
    ROOT / platform / "skills" / "soc-forensic-hunts"
    for platform in (".github", ".agents", ".claude")
)


class SocForensicHuntsContractTests(unittest.TestCase):
    def test_overlay_is_bounded_and_has_no_tool_preapproval(self) -> None:
        content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: soc-forensic-hunts", content)
        self.assertNotIn("allowed-tools:", content)
        for term in (
            "untrusted data",
            "Do not execute",
            "Do not recommend automatic containment",
            "LOCAL_ONLY",
            "framework overlay",
            "SOURCE FACT",
        ):
            self.assertIn(term, content)
        metadata = (CANONICAL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("Use $soc-forensic-hunts", metadata)
        self.assertFalse((CANONICAL / "scripts").exists())

    def test_references_and_adapters_match(self) -> None:
        expected = {
            "scope-and-evidence.md",
            "detection-validation.md",
            "attack-and-handoff.md",
        }
        self.assertEqual(
            expected,
            {item.name for item in (CANONICAL / "references").glob("*.md")},
        )
        detection = (CANONICAL / "references" / "detection-validation.md").read_text(
            encoding="utf-8"
        )
        for term in (
            "not probability",
            "or an authorization token",
            "calibration",
        ):
            self.assertIn(term, detection)

        canonical_files = {
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
            self.assertEqual(canonical_files, adapter_files)
            for path in canonical_files:
                self.assertEqual(
                    (CANONICAL / path).read_bytes(),
                    (adapter / path).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
