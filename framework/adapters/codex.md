# Codex adapter

Status: READY (RUNTIME_VALIDATED). On 2026-09-19, Codex on Windows loaded and natively started all ten user-scoped Nexora agent profiles after a complete client restart. All fifteen installed skills completed bounded synthetic method tests. The repaired package then passed 16/16 schema/installer checks and the complete 87/87 repository test suite. No fallback profile, customer data, production query, external API call, SSH connection or operational change was used.

The generated `.agents/skills` and `.codex/agents` adapters are runtime-discovered by the tested Codex client. Agent registration is snapshotted at client startup, so Codex must be fully restarted after installing or changing agent profiles. This evidence establishes discovery and bounded synthetic execution on the named environment; it is not a production, customer-data or general-behavior approval.

The first runtime pass exposed two packaging defects: shared JSON schemas were absent from the user-scoped skill installation, and an overlay skill retained stale files from an older install. The repository installer now replaces only named Nexora packages after backup and bundles the required SOC schemas inside `qradar-investigation`. Both defects were revalidated successfully after installation.

`READY` is scoped to the tested Codex integration with synthetic data. It is not authorization for customer data, production access, external writes, or a claim that local files imply local model inference. Those uses remain gated by approved local inference and technical egress controls.

Install or update for the current user from the repository root:

```text
python tools/sync_skills.py --prune
python tools/sync_agents.py
python tools/install_codex.py --dry-run
python tools/install_codex.py
```

Then fully restart Codex. Validation evidence is recorded in `docs/codex-runtime-validation.md`.
