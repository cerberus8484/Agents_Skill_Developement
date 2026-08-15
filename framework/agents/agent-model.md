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

## Security skill mapping

| Component | Role | Boundary |
|---|---|---|
| `security` | Method / reference | Supplies bounded security-review guidance; it does not scan, exploit, or modify. |
| `security-reviewer` | REVIEWER | Identifies and qualifies evidence-backed potential findings. |
| `code-reviewer` | REVIEWER | Uses the security method when a code review has a security-relevant focus. |
| `security-fixer` | Proposed EXECUTOR role | May implement an approved remediation only when separately authorized; it is not currently an installed agent. |

## Cross-Platform Definition of Done

For every newly reviewed or changed agent: canonical definition; Copilot custom-agent decision; Codex integration decision; Claude Code sub-agent decision; no manually divergent copies; contract tests; separate per-platform status; real runtime evidence where available; and updated security/data documentation. Missing hosts are UNTESTED until a test is attempted, then use the precise runtime-blocked status where applicable.
