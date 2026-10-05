# State and handoff

Create an initial machine-readable Investigation State compatible with the repository investigation schema:

- status: IN_PROGRESS;
- ticket ID and only supplied ticket context;
- evidence beginning with E001;
- completed check: Initial ticket triage;
- no inferred entities, hypotheses, findings, or completed results;
- one narrow next investigation step and explicit expected evidence.

**FRAMEWORK INTERPRETATION:** Triage may request that an analyst obtain particular data, but it does not create or execute an AQL/SPL query. qradar-investigation owns subsequent state updates and may make a query request. qradar-aql translates only that later request; security-event-analysis normalizes returned events; false-positive-analysis assesses supplied evidence; incident-summary reports the resulting state.

The handoff must identify evidence IDs, current gaps, the single next step, expected return material, and unresolved uncertainty.
