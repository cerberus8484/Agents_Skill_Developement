# Assessment Standard

Assess only the currently supplied evidence. The assessment must state:

- the activity or question being assessed;
- the evidence IDs supporting it;
- alternative explanations that remain plausible;
- material missing evidence;
- an evidence-based classification; and
- confidence using `confidence-standard.md`.

Permitted classifications are `UNASSESSED`, `UNKNOWN`, `INCONCLUSIVE`, `SUSPICIOUS`, `LIKELY_LEGITIMATE`, `CONFIRMED_LEGITIMATE`, `LIKELY_MALICIOUS`, and `CONFIRMED_MALICIOUS`. `LIKELY_LEGITIMATE` and `CONFIRMED_LEGITIMATE` require affirmative supporting evidence; theoretical plausibility is insufficient. `LIKELY_MALICIOUS` requires several attributable indicators; a known tool, suspicious token, or single weak indicator is insufficient.

## Detection validity and activity assessment

Keep these dimensions separate:

- `DETECTION VALIDITY`: `TRUE_POSITIVE`, `FALSE_POSITIVE`, or `UNDETERMINED` — whether the detection correctly identified its technical condition.
- `ACTIVITY ASSESSMENT`: one of the permitted classifications — what the evidence supports about the observed activity.

A technically correct detection can identify confirmed legitimate activity. Conversely, an activity classification must remain inconclusive when a parsing or data-quality issue undermines the technical condition used by the detection. Neither dimension authorizes automatic ticket closure.
