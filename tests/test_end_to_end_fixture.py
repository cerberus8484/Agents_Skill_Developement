import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent / "end-to-end-001"


class EndToEndFixtureTest(unittest.TestCase):
    def test_full_workflow_contract_preserves_traceability(self) -> None:
        self.assertTrue((ROOT / "workflow.md").is_file())
        expected = json.loads((ROOT / "expected.json").read_text(encoding="utf-8"))
        self.assertEqual(["E001", "E002", "E003"], expected["evidence_ids"])
        self.assertEqual(["H001", "H002"], expected["hypothesis_ids"])
        self.assertEqual(["F001"], expected["finding_ids"])
        self.assertEqual("TRUE_POSITIVE", expected["detection_validity"])
        self.assertEqual("CONFIRMED_LEGITIMATE", expected["activity_assessment"])
        self.assertTrue(expected["no_production_action"])
