# Secure coding: inputs, code execution, and secrets

Review untrusted data at each interpretation boundary: database query, shell command, template, file path, URL fetch, deserializer, parser, and authorization decision.

- Prefer parameterized APIs and typed or structured interfaces over string construction for queries and commands.
- Validate format, range, size, and ownership where the business rule needs them. Validation alone does not make string concatenation safe.
- Treat uploads, archives, file names, serialized objects, and redirects as separate attack surfaces; require explicit constraints and safe handling suited to the platform.
- For a detected secret, identify its type and location, redact its value, avoid echoing it into findings or logs, and recommend rotation or revocation through an authorized owner.
- Do not assume environment variables, an ORM, or a framework automatically provide appropriate protection; verify the relevant use.
- Review exception and error paths at security boundaries. A failed validation, authorization, parsing, or dependency operation must not silently grant access or expose sensitive internals; state uncertainty if the failure behavior is outside the artefact.

Potential mappings include CWE-20 (improper input validation), CWE-78/CWE-77 (command injection), CWE-89 (SQL injection), CWE-22 (path traversal), CWE-502 (deserialization), and CWE-200 (sensitive information exposure). Classify only when evidence matches.
