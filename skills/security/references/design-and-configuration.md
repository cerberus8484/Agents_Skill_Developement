# Design and configuration

- Review trust boundaries, assets, privileged operations, data flows, and abuse cases when design material is supplied. Missing design evidence is a handoff, not proof of insecure design.
- Inspect security-relevant configuration in scope: enabled defaults, debug behavior, exposed administration interfaces, CORS, TLS termination, headers, identity-provider settings, storage access, build configuration, and service permissions. Do not infer the live configuration from source code alone.
- Prefer secure defaults, explicit deny rules, least privilege, and documented exceptions. Whether a proposed control is appropriate depends on the system boundary and legitimate integration flows.
- Hand off cloud, network, CI/CD, identity, or production-configuration concerns to the accountable operator when those artefacts are absent.

OWASP Top 10:2025 includes Insecure Design and Security Misconfiguration. These categories guide review coverage; they do not turn an incomplete design or configuration review into a security assessment.
