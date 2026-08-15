# Web and network exposure

- For SSRF, trace whether an attacker can influence a server-side destination and whether validation, DNS resolution, redirects, protocols, egress controls, and metadata endpoints are in scope. An allowlist is only meaningful when it is applied at the effective destination boundary.
- For browser-facing content, inspect the output context. Encoding, sanitization, CSP, and framework behavior are context-specific and may complement rather than replace one another.
- For state-changing browser requests, assess the authentication mechanism, origin model, and framework protections before making a CSRF finding.
- Do not claim a network or cloud posture from application code alone. Hand off missing egress, TLS, gateway, or configuration evidence.

Potential mappings include CWE-918 (SSRF), CWE-79 (cross-site scripting), CWE-352 (CSRF), and CWE-16 (configuration).
