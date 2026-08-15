# Customer Data Local-Only Architecture

## Security invariant

`SIEM-AI-001`: Customer data must never be transmitted to or processed by an unapproved cloud AI service. `CUSTOMER_DATA` and `UNKNOWN` require `LOCAL_ONLY`; automatic cloud fallback is forbidden.

## Current state

The repository currently provides standards, synthetic policy contracts, skill references, and automated documentation tests. These are important design controls, but they do **not** technically route or block payloads.

**The current GitHub Copilot skill environment must not be considered a LOCAL_ONLY customer-data processing environment merely because these repository policies exist. Real customer data must not be introduced until the approved technical processing architecture enforces the required boundary.**

Current allowed repository use is development with synthetic material and testing with synthetic or demonstrably sanitized material, subject to enterprise policy.

## Future enforcement

```text
Analyst
  → Workspace classification
  → Data classification and policy gate
  → Secret / privacy-DLP gate
  → Enforced model router
      ├─ PUBLIC / SYNTHETIC / approved SANITIZED → enterprise-policy provider
      └─ CUSTOMER_DATA / UNKNOWN → local-only provider
                                      → local evidence store
```

The gate must run before prompt construction, model selection, telemetry, diagnostics, and egress. Customer workspaces default to `CUSTOMER_DATA`; unknown classification fails closed to the local-only path. If the local provider is unavailable, processing stops and informs the analyst. It must never fall back automatically to a cloud model.

## Required defense in depth before production approval

- Application-level classification, authorization, routing, and secret-redaction/block enforcement.
- Provider policy and credential separation preventing unapproved endpoints.
- DLP controls for prompts, telemetry, diagnostics, and attachments.
- Local-only model and evidence storage with access controls.
- Egress firewall, proxy deny rules, DNS restrictions, application allowlisting, provider endpoint blocking, and segmentation for customer mode.
- Minimal audit logs: decision metadata only, not raw prompts, events, identifiers, or secrets.
- Security testing proving deny behavior, no fallback, and no customer payload egress.

Skill instructions provide helpful defense in depth but are not a substitute for any control above.
