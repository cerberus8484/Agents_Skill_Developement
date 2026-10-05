# Detection validation and confidence

**SOURCE FACT:** Sigma's rule specification includes status, known false positives, and severity metadata. These fields support rule documentation and triage; they do not establish that a rule is calibrated for a particular environment.

**ESTABLISHED PRACTICE:** Validate each detection against versioned, representative test material and local telemetry before promotion. Keep true-positive, false-positive, edge, and evasion cases separate. Record the result, dataset limits, expected outcome, and owner.

**FRAMEWORK INTERPRETATION:** A confidence value is an explained prioritization signal, not probability, maliciousness, or an authorization token. Document its inputs, missing telemetry, contradictory evidence, environment-specific thresholds, and calibration evidence. Escalate uncertain or high-impact results to an analyst; do not prescribe containment solely from a score.

Do not treat a fixed false-positive target, an allowlist, a signed binary, an administrative account, a common tool, a common port, or a named threat family as sufficient evidence by itself.
