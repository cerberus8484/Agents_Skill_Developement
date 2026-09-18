"""Executable JSON Schema validation for Nexora investigation contracts."""

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, ValidationError
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_ROOT = ROOT / "schemas"


def load_schemas():
    schemas = {}
    for path in sorted(SCHEMA_ROOT.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        schemas[path.name] = schema
    return schemas


def build_registry(schemas):
    resources = [
        (schema["$id"], Resource.from_contents(schema))
        for schema in schemas.values()
    ]
    return Registry().with_resources(resources)


class JsonSchemaContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas = load_schemas()
        cls.registry = build_registry(cls.schemas)
        cls.evidence = {
            "id": "E001",
            "type": "event",
            "source": "synthetic-qradar",
            "title": "Synthetic PowerShell event",
            "received_at": "2026-09-18T12:00:00Z",
            "raw_content": "sanitized synthetic event",
        }
        cls.hypothesis = {
            "id": "H001",
            "statement": "Activity requires additional evidence.",
            "status": "ACTIVE",
            "confidence": "LOW",
            "supporting_evidence_ids": ["E001"],
            "contradicting_evidence_ids": [],
        }
        cls.finding = {
            "id": "F001",
            "title": "Unclassified activity",
            "classification": "UNKNOWN",
            "summary": "Available evidence is insufficient for a final assessment.",
            "evidence_ids": ["E001"],
            "hypothesis_ids": ["H001"],
            "confidence": "LOW",
        }

    def validator(self, name):
        return Draft202012Validator(
            self.schemas[name],
            registry=self.registry,
            format_checker=FormatChecker(),
        )

    def test_all_schemas_are_valid_draft_2020_12_documents(self):
        self.assertEqual(
            {"evidence.schema.json", "finding.schema.json", "hypothesis.schema.json", "investigation.schema.json"},
            set(self.schemas),
        )

    def test_valid_contract_objects_pass(self):
        self.validator("evidence.schema.json").validate(self.evidence)
        self.validator("hypothesis.schema.json").validate(self.hypothesis)
        self.validator("finding.schema.json").validate(self.finding)
        investigation = {
            "ticket": {"id": "SYN-001", "severity": "medium"},
            "status": "NEEDS_EVIDENCE",
            "entities": {"hosts": ["HOST-SYN-01"]},
            "evidence": [self.evidence],
            "completed_checks": ["Ticket fields normalized"],
            "open_checks": ["Collect process creation evidence"],
            "hypotheses": [self.hypothesis],
            "findings": [self.finding],
            "next_action": "Request sanitized process creation evidence.",
        }
        self.validator("investigation.schema.json").validate(investigation)

    def test_invalid_ids_formats_and_extra_fields_fail(self):
        invalid_evidence = {**self.evidence, "id": "evidence-1"}
        with self.assertRaises(ValidationError):
            self.validator("evidence.schema.json").validate(invalid_evidence)

        invalid_finding = {**self.finding, "unexpected": "not allowed"}
        with self.assertRaises(ValidationError):
            self.validator("finding.schema.json").validate(invalid_finding)

        invalid_timestamp = {**self.evidence, "received_at": "not-a-date"}
        with self.assertRaises(ValidationError):
            self.validator("evidence.schema.json").validate(invalid_timestamp)


if __name__ == "__main__":
    unittest.main()
