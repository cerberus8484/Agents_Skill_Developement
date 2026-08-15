# Phase 1 Coverage Matrix

All counts are derived from [`tests/manual-copilot-regression-inventory.csv`](../tests/manual-copilot-regression-inventory.csv) and validated by `tests/test_manual_regression_inventory.py`.

| Skill | Fixtures | Automated | Manual | Pass | Fail |
| --- | ---: | --- | --- | ---: | ---: |
| siem-ticket-triage | 3 | Yes | 0/3 blocked | 0 | 0 |
| qradar-investigation | 5 | Yes | 0/5 blocked | 0 | 0 |
| qradar-aql | 8 | Yes | 0/8 blocked | 0 | 0 |
| security-event-analysis | 10 | Yes | 0/10 blocked | 0 | 0 |
| false-positive-analysis | 12 | Yes | 0/12 blocked | 0 | 0 |
| incident-summary | 12 | Yes | 0/12 blocked | 0 | 0 |
| End-to-end workflow | 1 | Yes | 0/1 blocked | 0 | 0 |
| Data-protection policy contract | 10 | Yes | N/A (repository contract) | N/A | N/A |
| **SOC skill total** | **51** | **Yes** | **0/51 blocked** | **0** | **0** |
| **All automated fixtures** | **61** | **Yes** | **0/51 blocked** | **0** | **0** |

`PASS_WITH_NOTES` is also zero for the manual SOC skill set. The ten data-protection fixtures validate repository policy contracts, not live model output. There are no manual results to classify; `BLOCKED` does not imply pass or fail.
