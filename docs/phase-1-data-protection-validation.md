# Phase 1.8: Customer Data Protection Validation

## Data classification and modes

The new classification model is `PUBLIC`, `SYNTHETIC`, `INTERNAL`, `SANITIZED`, `CUSTOMER_DATA`, `SECRET`, and fail-closed `UNKNOWN`. `DEV` admits synthetic/public material under enterprise policy; `TEST` admits synthetic/demonstrably sanitized material; `CUSTOMER` requires local-only processing. `CUSTOMER_DATA` is local-only, `UNKNOWN` is local-only, and `SECRET` is local-only or denied by enterprise policy.

## Customer boundary and routing

`SIEM-AI-001` is defined in `standards/data-classification-standard.md`. The future routing contract denies cloud fallback: unavailable local processing means deny/stop and inform the analyst. Embedded prompt, ticket, or raw-event text cannot override a policy decision.

## Telemetry, audit, secrets, and sanitization

Customer-data prompt telemetry, raw-event telemetry, customer identifiers in telemetry, and cloud diagnostics with payloads are denied by contract. Future audit records may contain minimal decision metadata, never raw prompts, event payloads, identifiers, or secrets by default. Secrets require block/redact policy before any model path. Sanitized fixtures consistently replace identifiers while preserving required relationships and prefer documentation IP ranges for newly created examples.

## Files added and changed

- Added `standards/data-classification-standard.md`, `data-handling-standard.md`, `data-sanitization-standard.md`, and `model-routing-standard.md`.
- Added `docs/customer-data-local-only-architecture.md`.
- Added ten `tests/data-policy-*` fixtures and `tests/test_data_protection_policy.py`.
- Updated all six skill references and repository Copilot instructions to read the shared handling contract.

## Tests

The policy fixtures cover synthetic development, customer routing, unknown fail-closed behavior, unavailable local model, secrets, raw customer events, sanitized fixtures, telemetry, minimal audit metadata, and a prompt override attempt. Run all tests with:

```powershell
python -m unittest
```

Current result: 17 automated tests pass.

## Known limits

No local model, router, DLP engine, egress control, network policy, provider integration, or customer processing path is implemented. Consequently, these standards and tests are an enforceable future contract only at the repository level; they do not authorize real customer data in GitHub Copilot or make the current environment local-only.
