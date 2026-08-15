---
name: false-positive-analysis
description: Assess analyst-provided investigation evidence for detection validity and activity legitimacy or maliciousness without reanalyzing raw events. Use after triage, qradar-investigation, or security-event-analysis when evidence, findings, hypotheses, and gaps are available. Never close tickets, execute actions, or access production systems.
---

# False positive analysis

Read `standards/safety-rules.md`, `standards/data-handling-standard.md`, `standards/assessment-standard.md`, and `standards/confidence-standard.md`. This is a specialized assessment skill. Consume supplied evidence, findings, hypotheses, completed checks, and gaps; do not repeat raw-event normalization or create new technical facts absent from them.

Treat analyst context, change records, and maintenance claims as evidence of a claim, not independent verification. Never execute a query, call an API, access QRadar, SSH, or a jump server, change production state, or tell the analyst to close a ticket.

## Two-axis assessment

Always provide both dimensions independently:

- `DETECTION VALIDITY`: `TRUE_POSITIVE`, `FALSE_POSITIVE`, or `UNDETERMINED`.
- `ACTIVITY ASSESSMENT`: `CONFIRMED_LEGITIMATE`, `LIKELY_LEGITIMATE`, `INCONCLUSIVE`, `SUSPICIOUS`, `LIKELY_MALICIOUS`, or `CONFIRMED_MALICIOUS`.

`TRUE_POSITIVE` means the documented technical detection condition occurred; it does not mean malicious. `FALSE_POSITIVE` requires evidence that the expected technical condition did not occur, such as a proven raw-versus-parsed mismatch that explains the trigger. Legitimate activity does not itself make a detection false positive.

## Evidence threshold

Use only cited evidence IDs. Separate supporting and contradicting evidence for each axis. Assess data-quality, parsing, and timestamp concerns before relying strongly on affected evidence.

- Confirm legitimate activity only with affirmative contextual evidence that links the exact activity to an approved action, such as a verified change, expected account, matching time window, and matching command or task. An admin account, signed binary, known tool, service account, maintenance time, internal IP, or common port alone is insufficient.
- Confirm malicious activity only with multiple strong, attributable indicators that directly establish it. PowerShell, encoded commands, remote administration tools, unusual ports, or suspicious binaries alone are insufficient.
- Use `INCONCLUSIVE` when evidence cannot support a direction. Name the smallest material evidence gap.
- Do not ignore contradictions. Lower confidence or retain uncertainty when they materially affect the conclusion.

## Hypothesis impact and stop condition

Evaluate supplied `H###` hypotheses as `SUPPORTED`, `WEAKENED`, `REJECTED`, or `CONFIRMED` only to the degree the evidence permits. Do not replace the Investigation State.

Additional work has no immediate assessment value only when the supplied evidence strongly supports the chosen classification, contradictions are resolved or explained, and no material gap remains. State this as an assessment condition, never as a ticket-close instruction. For `INCONCLUSIVE` with material gaps, request the specific decision-relevant evidence.

## Required response

Use these headings in order:

```text
FALSE POSITIVE ANALYSIS
DETECTION VALIDITY
ACTIVITY ASSESSMENT
CONFIDENCE
SUPPORTING EVIDENCE
CONTRADICTING EVIDENCE
DATA QUALITY CONCERNS
HYPOTHESIS IMPACT
MISSING EVIDENCE
ASSESSMENT BASIS
RECOMMENDED INVESTIGATION INPUT
```

Every assertion in `ASSESSMENT BASIS` cites evidence IDs. In `RECOMMENDED INVESTIGATION INPUT`, end with a `RETURN TO INVESTIGATION` block containing both assessments, confidence, hypothesis updates, any remaining gap, and one suggested investigation area. Do not set the orchestrator's global next best step or close the ticket.
