# Confidence Standard

Confidence measures confidence in the current assessment, not incident severity and not likelihood of maliciousness.

| Level | Use when |
| --- | --- |
| `LOW` | Evidence is incomplete, ambiguous, unverified, or materially contradictory. The assessment is primarily a hypothesis. |
| `MEDIUM` | Several attributable evidence items support the assessment and key alternatives were considered, but important evidence or validation is still missing. |
| `HIGH` | Multiple independent, attributable sources directly support the assessment, contradictions are resolved or explained, and no material open question changes it. |

Never use `HIGH` merely because a rule fired, a detection has high severity, or a behavior is common. State the specific evidence and unresolved uncertainty beside the confidence.
