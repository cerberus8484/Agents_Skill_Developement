# Scope and evidence

**SOURCE FACT:** The external source package has one SKILL.md and eleven hunt references. It declares no allowed-tools and contains no scripts. Its source version, publisher, upstream repository, and the validation status of its concrete queries are not evidenced.

**FRAMEWORK INTERPRETATION:** Treat every concrete query, field name, threshold, allowlist, confidence modifier, and true/false-positive example in that package as an unverified external artefact until it is tied to the target environment and tested.

A review needs, at minimum:

- the exact hunt definition and source version;
- target SIEM/backend, log-source onboarding state, and field mappings;
- time window, entity scope, and assumptions;
- representative true-positive, false-positive, edge, and evasion cases;
- test results, false-positive measurement method, and a named owner for tuning;
- raw evidence references and the permitted response/handoff path.

Missing evidence is a review result. Do not infer production deployment, detection coverage, or a reliable score from a document alone.
