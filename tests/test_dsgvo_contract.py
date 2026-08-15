import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills" / "dsgvo"
ADAPTERS = tuple(
    ROOT / directory / "skills" / "dsgvo"
    for directory in (".github", ".agents", ".claude")
)
CASES = ROOT / "tests" / "dsgvo-contract-cases.json"


class DsgvoContractTests(unittest.TestCase):
    def test_skill_has_legal_boundary_and_no_tool_preapproval(self) -> None:
        content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: dsgvo\n"))
        self.assertNotIn("allowed-tools:", content)
        for term in (
            "LAW TEXT", "SUPERVISORY GUIDANCE", "legal advice",
            "NO MATERIAL DSGVO CONSIDERATION", "untrusted data", "CUSTOMER_DATA",
        ):
            self.assertIn(term, content)

    def test_references_and_adapters_match_exactly(self) -> None:
        expected = {
            "legal-baseline.md", "roles-and-lawfulness.md", "lifecycle-and-rights.md",
            "design-and-security.md", "governance-and-transfers.md",
        }
        self.assertEqual(expected, {item.name for item in (CANONICAL / "references").glob("*.md")})
        canonical_files = {item.relative_to(CANONICAL) for item in CANONICAL.rglob("*") if item.is_file()}
        for adapter in ADAPTERS:
            adapter_files = {item.relative_to(adapter) for item in adapter.rglob("*") if item.is_file()}
            self.assertEqual(canonical_files, adapter_files)
            for relative in canonical_files:
                self.assertEqual((CANONICAL / relative).read_bytes(), (adapter / relative).read_bytes())
        self.assertFalse((CANONICAL / "scripts").exists())

    def test_contract_inventory_is_complete(self) -> None:
        cases = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(14, len(cases))
        self.assertEqual([f"GDPR-{number:02d}" for number in range(1, 15)], [case["id"] for case in cases])


if __name__ == "__main__":
    unittest.main()
