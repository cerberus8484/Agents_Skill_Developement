# Scope and evidence

## Scope

Continue one investigation after triage using only analyst-supplied state and evidence. The skill preserves a reproducible record; it does not access QRadar, discover new data, or resolve the incident.

## Evidence contract

- Give each separately supplied record the next E### identifier; preserve existing identifiers.
- A FACT is directly stated by supplied evidence and cites E###.
- An OBSERVATION identifies a relevant pattern or inconsistency in facts and cites E###.
- An INFERENCE is a bounded connection between facts, names uncertainty, and cites E###.
- A HYPOTHESIS is a possible explanation, never a fact. Record support and contradiction separately.
- Keep analyst claims as analyst-note evidence, not as independently verified facts.
- Record missing raw payloads, query scope, timezone, log source, entities, results, or contradictory facts as gaps.

## State contract

Use schemas/investigation.schema.json together with the shared schemas for machine-readable state. Preserve completed checks and do not select one again without new evidence that justifies repetition. Use WAITING_FOR_EVIDENCE for a specific missing-evidence request and READY_FOR_ASSESSMENT only for a bounded handoff, never as an assessment decision.
