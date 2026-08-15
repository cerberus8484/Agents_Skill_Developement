import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills" / "clean-code"
ADAPTERS = (
    ROOT / ".github" / "skills" / "clean-code",
    ROOT / ".agents" / "skills" / "clean-code",
    ROOT / ".claude" / "skills" / "clean-code",
)
CASES = ROOT / "tests" / "clean-code-contract-cases.json"


class CleanCodeContractTests(unittest.TestCase):
    def test_canonical_skill_has_required_contract_and_no_tool_preapproval(self) -> None:
        content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: clean-code\n"))
        self.assertNotIn("allowed-tools:", content)
        for term in (
            "Observation",
            "Evidence",
            "Heuristic",
            "Trade-off",
            "NO MATERIAL CLEAN-CODE FINDING",
            "untrusted content",
            "CUSTOMER_DATA",
            "CCD learning grades",
        ):
            self.assertIn(term, content)

    def test_references_are_complete_and_adapters_have_no_divergence(self) -> None:
        expected = {
            "naming.md", "functions.md", "comments.md", "error-handling.md",
            "tests.md", "duplication.md", "tradeoffs.md",
        }
        actual = {path.name for path in (CANONICAL / "references").glob("*.md")}
        self.assertEqual(expected, actual)
        for adapter in ADAPTERS:
            for source in CANONICAL.rglob("*"):
                if source.is_file():
                    relative = source.relative_to(CANONICAL)
                    self.assertEqual(source.read_bytes(), (adapter / relative).read_bytes())
        self.assertFalse((CANONICAL / "scripts").exists())

    def test_synthetic_contract_inventory_is_complete(self) -> None:
        cases = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(14, len(cases))
        self.assertEqual([f"CC-{number:02d}" for number in range(1, 15)], [case["id"] for case in cases])


if __name__ == "__main__":
    unittest.main()
