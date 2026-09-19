# Nexora Agent Shield

Nexora Agent Shield is the offline policy gate for the generated IT/SOC agent
team. It independently compares the canonical team manifest and checked-in
platform adapters with an explicit least-privilege baseline.

## Run

```bash
python tools/run_agent_shield.py
```

The command exits non-zero when it detects:

- an agent without a Shield policy or a stale policy entry;
- unknown or policy-exceeding tool aliases in `team.json`;
- Copilot or Claude adapter tools that differ from the approved baseline;
- a Codex adapter identity mismatch or missing shared safety clauses;
- removal of required local-only, secret, trust, write, or verification clauses.

## Trust boundary

A passing report means the repository configuration matches Shield policy. It
does not prove what a host grants at runtime, block network egress, inspect
model-provider data flow, or verify that a model obeys the prompt.

Copilot and Claude expose per-agent tool lists that Shield can compare. The
current Codex repository adapter does not provide an enforceable per-agent tool
allowlist, so Shield reports that host control as `UNVERIFIED` for every
agent. This warning does not fail the static gate and must not be presented as a
runtime security pass.

Policy source: `standards/agent-shield-policy.json`.
