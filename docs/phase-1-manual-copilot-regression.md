# Phase 1 Manual Copilot Regression and Hardening

## Test inventory

The complete inventory is maintained in [`tests/manual-copilot-regression-inventory.csv`](../tests/manual-copilot-regression-inventory.csv). It contains all 51 synthetic scenarios and, for each one: ID, skill, fixture, purpose, expected and forbidden behavior reference, automated coverage, manual status, result, observed deviation, and required change.

## Automated coverage

`python -m unittest` completed successfully on 2026-08-14. The suite contains 15 tests and validates all 51 fixture contracts, skill-boundary wording, schema JSON, and the end-to-end contract. This is not evidence of live Copilot behavior.

## Manual Copilot coverage

Manual status is `BLOCKED` for all 51 scenarios; pass, fail, and pass-with-notes counts are therefore all zero.

The environment has authenticated GitHub CLI access, but both `gh copilot -- --help` and `gh copilot -p "Reply with exactly: COPILOT_READY"` returned `Copilot CLI not installed`. No interactive Copilot client or model output was available in this non-interactive workspace. A manual PASS, deviation, stability rating, or end-to-end result would therefore be unsupported and has not been recorded.

## Required manual protocol

On a Copilot-enabled interactive workstation:

1. Run `python -m unittest` first.
2. For each inventory row, provide only its `input.md` to the named skill and compare the response with `expected.json`.
3. Record output location, Copilot version, date, result (`PASS`, `PASS_WITH_NOTES`, `FAIL`, or `BLOCKED`), deviation severity, and smallest required change in the CSV or an approved internal record.
4. Run critical scenarios TRIAGE-002, TRIAGE-003, AQL-006, EVENT-003, FP-007, SUMMARY-005, SUMMARY-012, and E2E-001 three times each. Rate results `STABLE`, `MOSTLY_STABLE`, `VARIABLE`, or `UNACCEPTABLE`.
5. Do not store operational event data or unapproved Copilot outputs in this repository.

The critical scenarios cover incomplete evidence, prompt injection-like content, unknown custom properties, parsed/raw contradiction, detection validity ambiguity, missing evidence references, closure pressure, and full workflow continuity.

## Observed deviations and severity distribution

No Copilot output was obtained, so no deviation is evidenced. Distribution: `S0=0`, `S1=0`, `S2=0`, `S3=0`, `S4=0`, `unassessed=51`. This does **not** mean zero defects; it means the manual layer is not yet executed.

## Hardening changes

No skill or standard hardening was made in this phase. There is no observed Copilot deviation from which to infer the correct layer of change. The only additions are the complete inventory, its automated completeness test, and this protocol. This avoids prompt growth based on speculation.

## End-to-end behavior and remaining risks

The synthetic end-to-end fixture contract passes automated validation, but live end-to-end Copilot behavior is `BLOCKED`. Evidence continuity, finding continuity, hypothesis continuity, query-context continuity, assessment continuity, no invented facts, no production action, and no closure automation remain unconfirmed against a real Copilot response.

Remaining risks are model variability, local Copilot skill loading behavior, QRadar Custom Event Property syntax, local timezone semantics, and untested interaction across separately invoked skills.

## Phase 1 acceptance decision

**PHASE_1_NOT_ACCEPTED**

The automated foundation is green, but the acceptance gate requires manual Copilot execution of all fixtures, critical repeated tests, and a live end-to-end workflow. Those tests are blocked in the current environment, so Phase 1 cannot honestly be declared functionally validated.

No Phase 2 work should begin until the blocked manual validation is completed and any S3/S4 deviation is resolved or explicitly accepted.
