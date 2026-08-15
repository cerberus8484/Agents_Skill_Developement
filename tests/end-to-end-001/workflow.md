# Synthetic Phase 1 end-to-end workflow

1. `siem-ticket-triage` receives QR-E2E-001 and records `E001`: PowerShell alert on LAB-WS-10 at 2026-08-14T10:00:00Z.
2. `qradar-investigation` creates `H001` legitimate maintenance and `H002` suspicious execution, then requests process context for E001.
3. `qradar-aql` translates the constrained request into a read-only event-query proposal; the analyst executes it manually.
4. The analyst returns a synthetic query result. `security-event-analysis` records `E002`: command line matches change CHG-E2E-7, and `E003`: matching account and maintenance time. It creates `F001`, a PROCESS finding with the recorded command context.
5. `qradar-investigation` retains H001 and H002 and records process-context check completed.
6. `false-positive-analysis` preserves `TRUE_POSITIVE` detection validity and assesses `CONFIRMED_LEGITIMATE` activity from E001-E003 and the approved change context.
7. `incident-summary` reports the same IDs, hypothesis history, finding, and two-axis assessment. No production action is requested or performed.
