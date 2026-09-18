"""Tests for deterministic Nexora Agent Bench scoring."""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from jsonschema import ValidationError

from tools.run_benchmark import BENCHMARK_ROOT, run_suite, score_case


CASES = BENCHMARK_ROOT / "cases"
BASELINE = BENCHMARK_ROOT / "fixtures" / "baseline"


class NexoraAgentBenchTests(unittest.TestCase):
    def test_baseline_suite_passes_all_cases(self):
        report = run_suite(CASES, BASELINE)
        self.assertEqual("0.2", report["scoring_version"])
        self.assertEqual(3, report["cases"])
        self.assertEqual(3, report["passed"])
        self.assertEqual(100, report["score"])

    def test_forbidden_claim_is_a_critical_failure(self):
        case = CASES / "NAB-001.json"
        unsafe = json.loads((BASELINE / "NAB-001.json").read_text(encoding="utf-8"))
        unsafe["summary"] = "Production action completed."
        with TemporaryDirectory() as directory:
            response = Path(directory) / "NAB-001.json"
            response.write_text(json.dumps(unsafe), encoding="utf-8")
            result = score_case(case, response)
        self.assertFalse(result["passed"])
        self.assertEqual(["production action completed"], result["forbidden_hits"])
        self.assertEqual(0, result["checks"]["safety"])

    def test_missing_required_decision_is_a_critical_failure(self):
        case = CASES / "NAB-002.json"
        incomplete = json.loads((BASELINE / "NAB-002.json").read_text(encoding="utf-8"))
        incomplete["decisions"].remove("LOCAL_ONLY_REQUIRED")
        with TemporaryDirectory() as directory:
            response = Path(directory) / "NAB-002.json"
            response.write_text(json.dumps(incomplete), encoding="utf-8")
            result = score_case(case, response)
        self.assertFalse(result["passed"])
        self.assertEqual(["LOCAL_ONLY_REQUIRED"], result["missing_decisions"])
        self.assertEqual(0, result["checks"]["decisions"])

    def test_response_contract_rejects_unknown_fields_and_decisions(self):
        case = CASES / "NAB-002.json"
        invalid = json.loads((BASELINE / "NAB-002.json").read_text(encoding="utf-8"))
        invalid["secret_debug_trace"] = "not allowed"
        invalid["decisions"].append("INVENTED_DECISION")
        with TemporaryDirectory() as directory:
            response = Path(directory) / "NAB-002.json"
            response.write_text(json.dumps(invalid), encoding="utf-8")
            with self.assertRaises(ValidationError):
                score_case(case, response)

    def test_case_input_path_cannot_escape_case_directory(self):
        case_data = json.loads((CASES / "NAB-001.json").read_text(encoding="utf-8"))
        case_data["input_file"] = "../README.md"
        with TemporaryDirectory() as directory:
            case = Path(directory) / "NAB-999.json"
            case.write_text(json.dumps(case_data), encoding="utf-8")
            with self.assertRaises(ValidationError):
                score_case(case, BASELINE / "NAB-001.json")


if __name__ == "__main__":
    unittest.main()
