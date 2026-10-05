# Cryptography, data, logging, and supply chain

- Flag obsolete, home-grown, or misapplied cryptographic constructions only with evidence of the use and its security purpose. Do not prescribe algorithms or parameters without language, protocol, compliance, and threat-model context.
- Never place passwords, private keys, tokens, payment data, or unnecessary personal data in logs, URLs, client payloads, or diagnostic output.
- Treat dependency manifests, lock files, build scripts, package provenance, and update workflows as reviewable evidence. A static review cannot prove that all dependencies are vulnerability-free or uncompromised.
- Recommend tests for authentication failures, authorization boundaries, input handling, error paths, and security-sensitive changes when the test harness is available.

OWASP Top 10:2025 includes Cryptographic Failures, Software Supply Chain Failures, Security Logging and Alerting Failures, and Mishandling of Exceptional Conditions. Use these as an awareness vocabulary, not a certification checklist.
