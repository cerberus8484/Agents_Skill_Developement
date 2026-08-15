import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SKILLS = [
    "siem-ticket-triage",
    "qradar-investigation",
    "qradar-aql",
    "security-event-analysis",
    "false-positive-analysis",
    "incident-summary",
]


class DataProtectionPolicyTests(unittest.TestCase):
    def test_ten_policy_contract_scenarios_are_present(self) -> None:
        scenarios = sorted(ROOT.glob("data-policy-*"))
        self.assertGreaterEqual(len(scenarios), 10)
        for scenario in scenarios:
            with self.subTest(scenario=scenario.name):
                self.assertTrue((scenario / "input.md").is_file())
                expected = json.loads((scenario / "expected.json").read_text(encoding="utf-8"))
                self.assertIn(expected["decision"], {"ENTERPRISE_POLICY", "LOCAL_ONLY", "DENY_STOP", "BLOCK_OR_REDACT"})
                self.assertTrue(expected["cloud_fallback_forbidden"])

    def test_security_invariant_and_skill_references_are_present(self) -> None:
        classification = (ROOT.parent / "standards" / "data-classification-standard.md").read_text(encoding="utf-8")
        handling = (ROOT.parent / "standards" / "data-handling-standard.md").read_text(encoding="utf-8")
        routing = (ROOT.parent / "standards" / "model-routing-standard.md").read_text(encoding="utf-8")
        self.assertIn("SIEM-AI-001", classification)
        self.assertIn("CUSTOMER_DATA", classification)
        self.assertIn("LOCAL_ONLY", classification)
        self.assertIn("Skill instructions are not a security boundary", handling)
        self.assertIn("never fall back automatically to cloud", routing)
        for skill_name in SKILLS:
            content = (ROOT.parent / ".github" / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("standards/data-handling-standard.md", content)


if __name__ == "__main__":
    unittest.main()
