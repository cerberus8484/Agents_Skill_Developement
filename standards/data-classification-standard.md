# Data Classification Standard

## Security invariant

**SECURITY INVARIANT SIEM-AI-001:** Customer data must never be transmitted to or processed by an unapproved cloud AI service. `CUSTOMER_DATA` processing is `LOCAL_ONLY`. Unknown classification fails closed to `LOCAL_ONLY`. No automatic cloud fallback is permitted.

## Classifications

| Classification | Processing policy |
| --- | --- |
| `PUBLIC` | According to enterprise policy. |
| `SYNTHETIC` | Approved cloud processing may be used according to enterprise policy. |
| `INTERNAL` | According to enterprise policy. |
| `SANITIZED` | According to enterprise policy; sanitization must be demonstrable. |
| `CUSTOMER_DATA` | `LOCAL_ONLY`. Cloud processing is denied. |
| `SECRET` | `LOCAL_ONLY` or deny according to enterprise policy; never assume cloud approval. |
| `UNKNOWN` | `LOCAL_ONLY` until classification is resolved. |

Potential customer data includes customer identifiers, real users, emails, IP addresses, hostnames, domains, URLs, tickets, offenses, raw events, payloads, logs, security findings, case notes, screenshots, and topology information. This list is non-exhaustive. Classification must also use workspace, case, source, analyst declaration, and environment context; pattern matching alone cannot reliably identify customer data.

## Workspace inheritance

A customer investigation workspace defaults to `CUSTOMER_DATA`. Data in that workspace inherits this classification unless an approved policy explicitly records a narrower classification. Do not reclassify customer content as safe from its appearance alone.
