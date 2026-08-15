# Proposal status and output

## Status selection

| Status | Condition | AQL statement allowed? |
| --- | --- | --- |
| BLOCKED_MISSING_EVIDENCE | Purpose, Events scope, factual filter, defensible time boundaries, or another mandatory request fact is absent | No |
| TEMPLATE_ONLY | A required local property mapping is unknown or has no supplied validation evidence | No |
| REVIEW_REQUIRED | Request uses only documented baseline fields and no local validation evidence is supplied | Yes, one read-only proposal |
| LOCALLY_VALIDATED | Supplied evidence identifies the local QRadar environment/version, exact fields, timezone interpretation, validation date, and successful test result for this exact proposal | Yes, one read-only proposal |

## Validation evidence

LOCALLY_VALIDATED requires supplied local evidence, not an assertion by the model or IBM documentation. Record missing validation facts as unknown. Never upgrade the status based on a plausible field name, a copied query, or generic vendor examples.

## Non-executable template

For TEMPLATE_ONLY, QUERY TEMPLATE describes the intended event source, required filter concept, requested fields, and time bounds in prose. AQL PROPOSAL is NONE. This avoids emitting a copyable query that silently substitutes an unverified field mapping.
