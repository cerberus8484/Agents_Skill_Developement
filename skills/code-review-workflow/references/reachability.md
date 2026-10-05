# Reachability and counterevidence

FRAMEWORK INTERPRETATION, refined after the bounded Nexora validator trial. These are decision criteria, not benchmark results.

For a suspected boundary defect trace:
1. Entry point and input owner: external request, administrator, checked-in configuration, plugin, or unknown.
2. Earlier guards and transformation: type checks, allowlists, normalization, authorization, catalog validation.
3. Function behavior: exact accepted/rejected input and error path.
4. Downstream effect: persistence, response, command construction or another evidenced sink. A dangerous-sounding comment is not proof of that effect.

State where the chain stops. Use CONFIRMED_PATH for an evidenced relevant path; GUARD_BLOCKS_PATH when an inspected guard blocks this input on that path; PATH_UNKNOWN when context is missing. A blocked path does not prove all other callers safe.

Keep finding kind separate from severity:
- BEHAVIORAL_DEFECT: a mismatch with an evidenced contract.
- INTERNAL_ROBUSTNESS: an internal malformed configuration or direct-call edge case without demonstrated external reachability.
- SECURITY_RISK: an evidenced trust-boundary risk with stated preconditions; uncertainty need not suppress a potential finding.
- OPTIONAL_IMPROVEMENT: preference or improvement without an established failure.

Do not automatically downgrade configuration issues: user-uploaded schemas or mutable plugin catalogs can cross a trust boundary. Conversely, a synthetic direct invocation of a static internal schema compiler does not establish an HTTP exploit.

Normal conversion (for example numeric strings to numbers) is not a defect without a strict-type requirement or downstream mismatch. Name the contract before recommending rejection.

Separate direct-function regressions from entry-point tests. Neither substitutes for the other. Stop broad searching when the scoped path is resolved; list unexamined paths instead of implying whole-system coverage.
