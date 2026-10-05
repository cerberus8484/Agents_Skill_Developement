# Scope and evidence

**SOURCE FACT:** OWASP Top 10:2025 is an awareness document for web-application security risks. CWE is a weakness taxonomy, and NIST SSDF provides high-level secure-development practices. None establishes that a review of one artefact proves system security.

**FRAMEWORK INTERPRETATION:** A finding requires a concrete artefact observation and stated preconditions. Use “potential finding” when deployment behavior, reachability, trust boundaries, or compensating controls are unknown.

## Evidence discipline

- Distinguish a vulnerable pattern from a demonstrated exploit.
- State missing context: framework defaults, middleware, network egress policy, identity provider, deployment configuration, tests, and monitoring can change the conclusion.
- Do not turn a CWE or OWASP mapping into a severity guarantee.
- Escalate unknown architecture, cloud, or operational controls to the appropriate owner.

## References

- OWASP Top 10:2025: https://owasp.org/Top10/
- CWE Top 25: https://cwe.mitre.org/top25/
- NIST SP 800-218 SSDF: https://csrc.nist.gov/pubs/sp/800/218/final
- NIST source status: SP 800-218 Version 1.1 is FINAL (2022-02-03). SP 800-218 Rev. 1 / SSDF Version 1.2 is an INITIAL PUBLIC DRAFT (2025-12-17), not a final standard: https://csrc.nist.gov/pubs/sp/800/218/r1/ipd
