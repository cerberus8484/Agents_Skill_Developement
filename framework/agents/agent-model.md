# Agent data model

This is a preparation schema only. It does not migrate or redefine existing agents.

| Field | Meaning |
|---|---|
| Agent ID / display name | Stable identity. |
| Role | ADVISOR, REVIEWER, PLANNER, EXECUTOR, OPERATOR_ASSIST, OPERATOR, or ORCHESTRATOR. |
| Purpose | Bounded mission. |
| Capabilities / limitations | What it can and cannot do. |
| Skills / tools | Reusable method versus technical mechanism. |
| Permissions / autonomy | Environment-dependent authorization, documented separately from capability. |
| Inputs / outputs / handoffs | Operational contract. |
| Security and data constraints | Applicable policy and classification boundaries. |
| Platform implementations / tests / runtime validation | Evidence for each host. |
| Status | Evidence and maturity status. |

Example: code-simplifier is an EXECUTOR; whether it may write a file remains environment-dependent.
