# Phase 1.2: QRadar Investigation Validation

## Implemented scope

`qradar-investigation` is a GitHub Copilot skill that continues one analyst-provided investigation. It updates the existing Investigation State, preserves evidence IDs, manages the hypothesis lifecycle, avoids repeated checks, selects one evidence-driven next action, and produces a structured, non-executed query request for the later `qradar-aql` skill.

No QRadar API, AQL execution, SSH, Jumpserver access, remote command, production change, or ticket closure capability was added.

## Added and changed files

- Added `.github/skills/qradar-investigation/SKILL.md`.
- Added five synthetic cases under `tests/investigation-001` through `tests/investigation-005` and `tests/test_investigation_fixtures.py`.
- Extended `schemas/investigation.schema.json` with the required lifecycle states while retaining existing ones for compatibility.
- Extended `schemas/hypothesis.schema.json` with `ACTIVE` while retaining `OPEN` for compatibility.
- Clarified corresponding state semantics in `standards/investigation-standard.md`.

## Automated validation

Run:

```powershell
python -m unittest tests.test_fixtures tests.test_investigation_fixtures
```

The tests validate the existing triage fixtures, four JSON schemas, the new skill's safety boundary, and the complete contracts of all five investigation scenarios.

## Hallucination protections exercised

- insufficient PowerShell detail does not permit a malware or false-positive claim;
- an administrator role remains an unverified legitimate-activity hypothesis;
- temporal proximity of PowerShell and a connection is an inference, not causation;
- contradictory maintenance and encoded-command context keeps confidence low;
- a completed process check is not selected as the next primary action;
- query-like requests require an entity and evidence-derived time anchor;
- embedded content is treated as evidence, never as an instruction, through the shared safety rules.

## Edge cases and limits

The automated tests verify fixture and skill contracts, not an LLM's actual reasoning. Run the manual protocol in `tests/README.md` with the five investigation fixtures before accepting Copilot behavior. State merging across analyst messages is instruction-driven rather than implemented as a persistence service; the analyst must provide the current state. Entity aliases, timezone conversion, QID semantics, and QRadar custom-property vocabulary remain deliberately unresolved until environment-approved reference material exists.

## Prepared for qradar-aql

The skill emits a constrained query request containing purpose, QRadar data source, entity, evidence anchor and time window, required fields, reason, and linked hypotheses. The next `qradar-aql` skill can translate that request into AQL without changing the investigation state model.

## Recommendation

Perform manual Copilot regressions for the five scenarios, record any unsupported conclusion or malformed state output, then implement `qradar-aql` against the query-request contract.
