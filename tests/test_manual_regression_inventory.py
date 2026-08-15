import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "manual-copilot-regression-inventory.csv"
EXPECTED_SKILL_COUNTS = {
    "siem-ticket-triage": 3,
    "qradar-investigation": 5,
    "qradar-aql": 8,
    "security-event-analysis": 10,
    "false-positive-analysis": 12,
    "incident-summary": 12,
    "end-to-end": 1,
}


class ManualRegressionInventoryTests(unittest.TestCase):
    def test_inventory_matches_all_synthetic_scenarios(self) -> None:
        with INVENTORY.open(encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(51, len(rows))
        counts = {skill: 0 for skill in EXPECTED_SKILL_COUNTS}
        for row in rows:
            self.assertIn(row["skill"], counts)
            self.assertTrue((ROOT / row["fixture"]).is_dir())
            self.assertEqual("YES", row["automated_coverage"])
            self.assertIn(row["manual_copilot_status"], {"PASS", "PASS_WITH_NOTES", "FAIL", "BLOCKED"})
            counts[row["skill"]] += 1
        self.assertEqual(EXPECTED_SKILL_COUNTS, counts)


if __name__ == "__main__":
    unittest.main()
