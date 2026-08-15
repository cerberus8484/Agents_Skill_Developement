# Phase 1.4: Security Event Analysis Validation

## Scope

`security-event-analysis` analyzes analyst-provided QRadar rows, raw events, tables, and structured data as an evidence producer for `qradar-investigation`. It normalizes only supplied fields, preserves provenance, creates sequential evidence and finding IDs, identifies data-quality issues, and produces technical findings without taking ownership of incident disposition or next best action.

No query execution, API integration, SSH, Jumpserver access, remote command, production change, or ticket closure capability was added.

## New and changed files

- Added `.github/skills/security-event-analysis/SKILL.md`.
- Added `tests/test_event_analysis_fixtures.py` and ten fixtures under `tests/event-analysis-001` through `tests/event-analysis-010`.
- Extended `schemas/finding.schema.json` with an optional, backward-compatible `category` property for technical finding types.
- Updated the repository and test READMEs for the new skill and unified test command.

## Supported event inputs and provenance

The skill supports QRadar query rows, one or more raw events, structured event data, pasted tables, and analyst context. Every relevant source becomes a separately referenced evidence item whose normalized facts remain tied to its original row or payload. Existing evidence IDs are preserved, and new IDs begin after the highest supplied ID.

## Raw versus parsed, timestamps, and duplicates

Raw and parsed values are preserved independently. Their disagreement becomes a data-quality or parsing finding without attributing a cause. Timestamp handling distinguishes device/event, SIEM receive, stored/start, and analyst-provided time where present; timezone absence and extreme discrepancies are explicit issues, not inferred causes. Exact duplicates require identical supplied records; near-time events remain related or separate unless evidence supports more.

## Hallucination boundaries tested

The ten fixtures cover complete and missing QRadar rows, raw/parsed source-IP conflict, historical device time, PowerShell alone, EncodedCommand, process/network temporal proximity, repeated authentication failures, exact duplicates, and continuation after `E018`.

They verify that fields are not invented; PowerShell and EncodedCommand alone do not prove malware; temporal correlation does not prove causation; authentication failures do not prove compromise; and data-quality evidence does not prove a parser defect.

## Schema change

`finding.schema.json` now allows an optional `category` from `SECURITY_RELEVANT`, `DATA_QUALITY`, `PARSING`, `TIMESTAMP`, `PROCESS`, `AUTHENTICATION`, `NETWORK`, `ENTITY`, `DUPLICATE`, and `UNKNOWN`. Existing valid findings do not need a category and remain compatible.

## Validation and limits

Run all checks:

```powershell
python -m unittest
```

Automated tests validate fixture contracts and skill safety wording, not LLM reasoning or real parser behavior. Manually run the ten cases with Copilot before acceptance. Current limits include no full syslog/CEF/LEEF parser, no validated local QRadar custom-property mapping, no persistence service for state, and no automatic correlation beyond the supplied material.

## Recommended next step

After manual regression, implement `false-positive-analysis` using evidence and findings produced here. It should consume the structured records rather than duplicate raw-event normalization.
