# Codex runtime validation

## Decision

Status: **READY** for the validated Codex integration using synthetic data.

This status does not authorize customer data, production access, external writes, live SIEM queries, SSH, containment, ticket closure, or unverified cloud processing. A local file, CLI, MCP server, skill or agent profile does not prove local model inference or network isolation.

## Environment and evidence

- Date: 2026-09-19
- Platform: Codex on Windows
- Installation scope: user-scoped Nexora skills and Codex agent profiles
- Data: synthetic only
- Profile fallback: none
- Replacement agents: none

## Results

| Gate | Result |
|---|---:|
| Schema and installer tests | 16/16 PASS |
| Complete repository test suite | 87/87 PASS |
| Native Nexora agent starts | 10/10 PASS |
| Installed Nexora skill method tests | 15/15 PASS |
| Nexora Agent Shield | PASS, 38 checks |
| Nexora Agent Bench | PASS, 3/3 cases, score 100 |

The missing development dependency `jsonschema[format]` was installed from the versioned `requirements-dev.txt` before the complete test run.

## Defect closure

The initial runtime run found missing packaged schemas and stale files left in `soc-forensic-hunts`. The repaired installer now backs up and completely replaces only named Nexora packages while preserving unrelated personal skills and agents. The four SOC schemas are bundled inside `qradar-investigation`. Both defects passed the post-install validation.

The initial `unknown agent_type` results were caused by installing profiles during an already running Codex session. A complete client restart registered all ten profiles successfully.

## Remaining controls

- Runtime tool enforcement, network egress and model-side data flow are not proven by prompt contracts or these tests.
- CUSTOMER_DATA and UNKNOWN remain LOCAL_ONLY and require approved local inference plus technical enforcement before use.
- Production queries and operational actions remain outside the validated scope.
- Changes to agent profiles require a complete Codex restart and a new bounded regression run.
