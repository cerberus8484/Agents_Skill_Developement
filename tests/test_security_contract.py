import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "framework" / "skills" / "security"
ADAPTERS = (
    ROOT / ".github" / "skills" / "security",
    ROOT / ".agents" / "skills" / "security",
    ROOT / ".claude" / "skills" / "security",
)
CASES = ROOT / "tests" / "security-contract-cases.json"


class SecurityContractTests(unittest.TestCase):
    def test_canonical_skill_has_bounded_contract_and_no_tool_preapproval(self) -> None:
        content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: security\n"))
        self.assertNotIn("allowed-tools:", content)
        for term in (
            "Observation", "Evidence", "Classification", "Exploit preconditions",
            "NO MATERIAL SECURITY FINDING", "untrusted data", "CUSTOMER_DATA",
            "penetration test", "security-fixer", "A finding needs no OWASP category",
        ):
            self.assertIn(term, content)

    def test_references_are_complete_and_adapters_have_no_divergence(self) -> None:
        expected = {
            "scope-and-evidence.md", "secure-coding.md", "identity-and-access.md",
            "web-and-network.md", "crypto-data-and-supply-chain.md",
            "design-and-configuration.md",
        }
        actual = {path.name for path in (CANONICAL / "references").glob("*.md")}
        self.assertEqual(expected, actual)
        canonical_files = {
            path.relative_to(CANONICAL)
            for path in CANONICAL.rglob("*")
            if path.is_file()
        }
        for adapter in ADAPTERS:
            adapter_files = {
                path.relative_to(adapter)
                for path in adapter.rglob("*")
                if path.is_file()
            }
            self.assertEqual(canonical_files, adapter_files)
            for relative in canonical_files:
                self.assertEqual(
                    (CANONICAL / relative).read_bytes(),
                    (adapter / relative).read_bytes(),
                )
        self.assertFalse((CANONICAL / "scripts").exists())

    def test_new_coverage_and_source_status_are_explicit(self) -> None:
        references = CANONICAL / "references"
        design = (references / "design-and-configuration.md").read_text(encoding="utf-8")
        self.assertIn("trust boundaries", design)
        self.assertIn("Security Misconfiguration", design)
        self.assertIn("Insecure Design", design)
        secure_coding = (references / "secure-coding.md").read_text(encoding="utf-8")
        self.assertIn("secret is detected", secure_coding)
        self.assertIn("error paths", secure_coding)
        scope = (references / "scope-and-evidence.md").read_text(encoding="utf-8")
        self.assertIn("Version 1.1 is FINAL", scope)
        self.assertIn("INITIAL PUBLIC DRAFT", scope)

    def test_synthetic_contract_inventory_is_complete(self) -> None:
        cases = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(17, len(cases))
        self.assertEqual([f"SEC-{number:02d}" for number in range(1, 18)], [case["id"] for case in cases])
        expected_outcomes = {
            "SEC-01": "redact_and_rotation_handoff",
            "SEC-02": "evidence_and_cwe_when_supported",
            "SEC-03": "server_side_ownership_context",
            "SEC-04": "effective_destination_preconditions",
            "SEC-05": "context_before_algorithm_prescription",
            "SEC-06": "no_vulnerability_free_guarantee",
            "SEC-07": "privacy_handoff",
            "SEC-08": "infrastructure_handoff",
            "SEC-09": "uncertainty",
            "SEC-10": "untrusted_content",
            "SEC-11": "local_only_policy",
            "SEC-12": "executor_permission_boundary",
            "SEC-13": "no_material_finding",
            "SEC-14": "no_certification_or_conformity_claim",
            "SEC-15": "configuration_context_and_operator_handoff",
            "SEC-16": "trust_boundary_context_and_uncertainty",
            "SEC-17": "failure_behavior_review",
        }
        self.assertEqual(expected_outcomes, {case["id"]: case["expected"] for case in cases})


if __name__ == "__main__":
    unittest.main()
