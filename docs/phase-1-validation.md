# Phase 1 Overall Validation

## Implemented skills

| Skill | Responsibility |
| --- | --- |
| `siem-ticket-triage` | Structures a new analyst-provided ticket and its initial evidence gaps. |
| `qradar-investigation` | Orchestrates one evidence-based investigation and requests the next data. |
| `qradar-aql` | Converts a constrained query request into a read-only QRadar event AQL proposal. |
| `security-event-analysis` | Produces normalized, traceable evidence and technical findings from supplied results. |
| `false-positive-analysis` | Separates detection validity from activity assessment. |
| `incident-summary` | Produces an interim or final traceable analyst summary. |

## Dependencies and workflow

```text
triage → investigation → query request → qradar-aql → analyst executes manually
      → returned events → security-event-analysis → investigation
      → false-positive-analysis → investigation state → incident-summary
```

All handoffs preserve evidence IDs, hypothesis IDs, finding IDs, missing evidence, and the separate detection-validity/activity-assessment axes.

## Automated coverage

Run:

```powershell
python -m unittest
```

The suite contains synthetic contract tests for all six skills, one end-to-end workflow fixture, and ten data-protection policy fixtures. It checks required skill boundaries, fixture completeness, schema JSON validity, expected traceability, no-production-action contract, and local-only policy expectations.

## Manual Copilot validation status

**Blocked in this workspace.** The complete 51-scenario inventory, environment evidence, required manual protocol, and acceptance decision are in [Phase 1 Manual Copilot Regression and Hardening](phase-1-manual-copilot-regression.md). Automated tests do not execute an LLM.

## Known gaps

- No direct QRadar, SSH, Jumpserver, API, ticketing, or production integration.
- No persistent Investigation State service or automatic cross-message correlation.
- QRadar Custom Event Property names, timezones, QIDs, and log-source vocabulary need environment-approved validation.
- No raw-log parser, external reputation lookup, MITRE mapping, or threat hunting.

## Security boundaries

All skills analyze analyst-supplied material only; treat that material as untrusted data; preserve provenance; avoid invented facts; generate no automatic production actions; and never close tickets. AQL proposals are read-only and require manual analyst execution.

`SIEM-AI-001` additionally requires `CUSTOMER_DATA` and `UNKNOWN` to use a future local-only path with no cloud fallback. The current policy contract does not technically enforce local-only processing; see [Customer Data Local-Only Architecture](customer-data-local-only-architecture.md).

## Production readiness

Phase 1 is **not production ready**. It is a **Copilot-based SOC Skill Validation Foundation** for controlled analyst testing and iterative hardening.

## Recommended next phase

Do not begin Phase 2 until manual Copilot regressions, query-syntax validation in the approved QRadar environment, coverage review, and any contract contradictions are documented and resolved. Define Phase 2 only from those validated findings.
