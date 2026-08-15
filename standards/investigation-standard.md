# Investigation Standard

## Purpose

Every skill records the current state of one ticket or investigation. It is an analyst aid, not an autonomous decision-maker.

## Required output order

1. `FACTS` — direct, attributable statements from supplied evidence only. Cite evidence IDs.
2. `OBSERVATIONS` — technical patterns or inconsistencies derived from facts; cite evidence IDs.
3. `HYPOTHESES` — possible explanations, each with a unique `H###` ID. A hypothesis is never a fact.
4. `SUPPORTING EVIDENCE` — evidence IDs and why they support a hypothesis.
5. `CONTRADICTING EVIDENCE` — evidence IDs and why they weaken a hypothesis.
6. `MISSING EVIDENCE` — information needed to improve the assessment.
7. `NEXT INVESTIGATION STEP` — one highest-value analyst action, including purpose and expected result.
8. `NEXT QUERY` — only when a query would obtain the missing evidence. Queries are suggestions, never executed.
9. `ASSESSMENT` — current, scoped assessment with uncertainty stated.
10. `CONFIDENCE` — `LOW`, `MEDIUM`, or `HIGH`, using `confidence-standard.md`.

## Investigation State

Use the JSON schema in `schemas/investigation.schema.json` as the canonical machine-readable state. Preserve original evidence and timestamps. Assign IDs sequentially:

- Evidence: `E001`, `E002`, …
- Hypotheses: `H001`, `H002`, …
- Findings: `F001`, `F002`, …

Reference evidence IDs in all facts, observations, hypothesis assessments, and findings. If a supplied datum cannot be assigned an ID, identify it as unstructured input and request clarification rather than silently changing it.

## State transitions

- Start at `NEW`; use `IN_PROGRESS` after triage begins.
- Add completed checks only after the analyst has supplied their result.
- Move an item from open checks to completed checks only with evidence or an explicit analyst statement.
- Use `NEEDS_EVIDENCE` or `WAITING_FOR_EVIDENCE` if a material question cannot be evaluated; the latter is preferred when a specific request has been issued to the analyst.
- Use `READY_FOR_ASSESSMENT` when the AI state has a sufficiently bounded basis for an assessment, but the analyst has not completed the investigation.
- Use `COMPLETE` or `COMPLETED` only when no material investigation question remains. Neither state closes a productive ticket.
