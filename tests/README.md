# Triage Acceptance Tests

These fixtures are synthetic and contain no production data. They are contract tests for the `siem-ticket-triage` skill, not an automated claim that an LLM has reasoned correctly.

## Automated checks

Run:

```powershell
python -m unittest
```

This verifies that every fixture has input, an explicit expected contract, at least one forbidden conclusion, and all required expectation categories.

## Manual regression protocol

For each triage ticket, provide only `input.md` to Copilot and invoke `/siem-ticket-triage`. For each investigation scenario, invoke `/qradar-investigation` with only that scenario's input. For each AQL scenario, invoke `/qradar-aql` with only that scenario's input. For each event-analysis scenario, invoke `/security-event-analysis` with only that scenario's input. For each assessment scenario, invoke `/false-positive-analysis` with only that scenario's input. For each summary scenario, invoke `/incident-summary` with only that scenario's input.

Pass only when the response:

1. uses the required headings of the invoked skill;
2. identifies every expected fact without inventing values;
3. asks for all expected missing evidence;
4. proposes an expected investigation step and only the allowed query type;
5. avoids each forbidden conclusion; and
6. keeps the expected assessment and confidence boundary.

Record the Copilot version, date, prompt, full response, and pass/fail rationale outside this repository if the response could include operational information.
