# Phase 1.5: False Positive Analysis Validation

## Scope

`false-positive-analysis` is a specialized assessment skill that consumes supplied triage, investigation, evidence, findings, hypotheses, and gaps. It does not duplicate raw-event analysis, change the Investigation State, execute queries, access systems, make production changes, or close tickets.

## Assessment model

The activity axis supports `CONFIRMED_LEGITIMATE`, `LIKELY_LEGITIMATE`, `INCONCLUSIVE`, `SUSPICIOUS`, `LIKELY_MALICIOUS`, and `CONFIRMED_MALICIOUS`. Confidence remains `LOW`, `MEDIUM`, or `HIGH` and is not a numeric score.

The separate detection-validity axis supports `TRUE_POSITIVE`, `FALSE_POSITIVE`, and `UNDETERMINED`. A true-positive detection can identify legitimate activity; legitimate activity does not make a detection false positive. A detection false positive requires evidence that its technical condition did not occur or that a validated data/parsing issue caused the trigger.

## New and changed files

- Added `.github/skills/false-positive-analysis/SKILL.md`.
- Added `tests/test_false_positive_fixtures.py` and twelve cases under `tests/false-positive-001` through `tests/false-positive-012`.
- Extended `standards/assessment-standard.md` with the two-axis definition and two additional assessment classifications.
- Extended `schemas/finding.schema.json` with `INCONCLUSIVE` and `LIKELY_MALICIOUS`; prior classifications remain valid.
- Updated repository and test READMEs for the new skill.

## Tested false-positive boundaries

The fixtures prove that an administrator account, maintenance window, Microsoft signature, known tool, PowerShell, or EncodedCommand alone cannot establish the final activity classification. They also test confirmed maintenance, a technically true-positive but legitimate detection, potential parsing-caused triggers, contradictory change evidence, sparse evidence, data-quality concerns, and a synthetic strong malicious chain.

## Evidence, hypotheses, and data quality

Each output must cite evidence IDs, retain both supporting and contradicting evidence, identify the smallest decision-relevant gap, and express impact on supplied hypotheses without owning the Investigation State. Parsing, timestamp, and data-quality findings reduce what can be inferred from the affected evidence and can leave both axes undetermined.

## Validation

Run all Phase 1 checks:

```powershell
python -m unittest
```

Automated tests verify the twelve fixture contracts and required skill safety boundaries. They do not execute an LLM or validate an analyst's local workflow. Manually run every fixture through Copilot before accepting the model behavior.

## Known limits and edge cases

The skill depends on analyst-provided evidence and cannot verify change tickets, signatures, malware reports, or environment context. It deliberately does not assign evidence weights numerically or perform external reputation lookups. Mixed activities, partially authorized scripts, inherited service accounts, and disagreements between authoritative sources require further analyst context.

## Recommendation

After manual regression, implement `incident-summary` as the final Phase 1 consumer: it should consolidate existing state, evidence, findings, and two-axis assessment without reanalyzing or changing them.
