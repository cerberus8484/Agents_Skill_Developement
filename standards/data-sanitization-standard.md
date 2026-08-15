# Data Sanitization Standard

Use only `SYNTHETIC` or demonstrably `SANITIZED` material in cloud-enabled development or test paths. Sanitization must remove or consistently replace customer names, usernames, emails, hostnames, IPs, domains, URLs, ticket and asset IDs, and free-text customer references.

Preserve test-relevant relationships with stable aliases. Example: `jsmith`, `ACME-DC01`, and `10.48.21.17` become `USER-001`, `HOST-001`, and `192.0.2.17`. Keep the mapping outside the cloud-enabled fixture repository and do not include original-to-alias mappings in prompts, fixtures, telemetry, or audit records.

Prefer documentation ranges `192.0.2.0/24`, `198.51.100.0/24`, and `203.0.113.0/24` for newly created synthetic examples. Existing synthetic fixtures are not retroactively changed without a regression review. Sanitization is a controlled process with human review; regex replacement alone is insufficient.
