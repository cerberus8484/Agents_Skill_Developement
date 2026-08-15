# Identity and access

Authentication establishes an asserted identity; authorization decides whether that identity may perform an action on a particular resource.

- Look for server-side checks on state-changing and sensitive operations.
- Review object ownership and tenant boundaries when identifiers are user-controlled or derived from requests.
- Make failure behavior explicit. A failed policy lookup must not silently grant access.
- Do not prescribe one token storage mechanism without the application architecture and threat model. Review session lifetime, transport, revocation, browser behavior, and server controls together.
- Treat missing evidence of authorization as an uncertainty when shared middleware, policy engines, or database controls are outside the artefact.

Potential mappings include CWE-862 (missing authorization), CWE-863 (incorrect authorization), CWE-639 (authorization bypass through user-controlled key), CWE-306 (missing authentication), and CWE-284 (improper access control).
