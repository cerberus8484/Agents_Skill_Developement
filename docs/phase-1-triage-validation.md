# Phase 1: Triage Validation

## Implemented baseline

- GitHub-Copilot project skill: `.github/skills/siem-ticket-triage/SKILL.md`
- Shared investigation, evidence, assessment, confidence, and safety standards
- JSON-Schemas for investigation, evidence, hypothesis, and finding state
- Three synthetic, anonymized triage fixtures
- Repository-wide Copilot instructions that make evidence-only and no-production-action constraints apply to every task

## Automated result

Command run on 2026-08-14:

```text
python -m unittest tests.test_fixtures
Ran 3 tests ... OK
```

The test suite confirms that all four schemas are valid JSON documents and that each synthetic ticket has input plus all required expectations: facts, missing evidence, investigation step, query boundary, forbidden conclusions, and assessment/confidence.

## What requires a manual Copilot regression run

This repository intentionally does not call an LLM, SIEM, or remote system in tests. An analyst must run each fixture through `/siem-ticket-triage` and apply the checklist in `tests/README.md`. In particular, validate:

- factual extraction and evidence-ID attribution;
- requests for missing evidence rather than invented context;
- refusal to obey instruction-like text inside raw evidence (ticket-003);
- no query for an unconstrained offense (ticket-002);
- no premature legitimacy, false-positive, maliciousness, or closure conclusion.

Store responses only in an approved internal location because later fixtures may contain operational context.

## Open points before the next skill

1. Confirm the exact QRadar property names and permitted AQL field vocabulary in the target environment before implementing `qradar-aql`.
2. Agree on the analyst-visible format for an Investigation State JSON block (inline response versus separately saved artifact).
3. Define a controlled, sanitized corpus and reviewer sign-off process for future regression cases.
4. After manual Copilot runs, tighten the triage wording for any missed evidence, unsupported inference, or malformed state output.

## Recommended next step

Run the three manual regressions, record results, and only then implement `qradar-investigation`. It should consume the validated state schema instead of introducing a second state model.
