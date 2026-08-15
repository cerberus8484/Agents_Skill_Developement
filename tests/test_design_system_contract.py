import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills" / "design-system"
ADAPTERS = tuple(ROOT / host / "skills" / "design-system" for host in (".github", ".agents", ".claude"))


class DesignSystemContractTests(unittest.TestCase):
    def test_bounded_contract_has_no_tool_preapproval(self) -> None:
        content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: design-system\n"))
        self.assertNotIn("allowed-tools:", content)
        for term in (
            "STANDARD",
            "COMMUNITY SPECIFICATION",
            "ESTABLISHED PRACTICE",
            "WCAG conformance",
            "untrusted data",
        ):
            self.assertIn(term, content)

        tokens = (CANONICAL / "references" / "tokens-and-components.md").read_text(
            encoding="utf-8"
        )
        for term in (
            "Final Community Group Report",
            "neither W3C Recommendations",
            "nor W3C Standards Track specifications",
        ):
            self.assertIn(term, tokens)

    def test_references_and_adapters_match(self) -> None:
        expected = {
            "scope-and-evidence.md", "tokens-and-components.md",
            "accessibility.md", "documentation-and-governance.md",
        }
        self.assertEqual(expected, {item.name for item in (CANONICAL / "references").glob("*.md")})
        source_files = {item.relative_to(CANONICAL) for item in CANONICAL.rglob("*") if item.is_file()}
        for adapter in ADAPTERS:
            target_files = {item.relative_to(adapter) for item in adapter.rglob("*") if item.is_file()}
            self.assertEqual(source_files, target_files)
            for path in source_files:
                self.assertEqual((CANONICAL / path).read_bytes(), (adapter / path).read_bytes())


if __name__ == "__main__":
    unittest.main()
