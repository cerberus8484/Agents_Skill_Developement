# Orchestration and handoffs

## One proposed next step

The NEXT INVESTIGATION STEP is a single evidence-supported proposed action. It must identify the gap or competing hypotheses it distinguishes and the evidence expected. It is not an assertion that the action is objectively or globally optimal.

## Route by responsibility

| Need | Handoff | This skill does not do it |
| --- | --- | --- |
| Structured QRadar data request | qradar-aql | Generate or execute AQL |
| Raw events, payload parsing, field normalization, technical correlation | security-event-analysis | Analyze raw payloads |
| Detection validity or false-positive/activity assessment | false-positive-analysis | Decide legitimacy or maliciousness |
| Investigation reporting | incident-summary | Create incident summary |
| Containment, remediation, ticket change, production action | Authorized human / future authorized operator | Act or authorize action |

## Query request boundary

When the next step requires QRadar evidence, emit a not-executed request only after an entity and evidence-anchored time window are supplied. The request is input for qradar-aql, not a query or a command.
