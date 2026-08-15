# Scope and evidence

**SOURCE FACT:** A ticket or offense is a report of an alerting condition and its available context. It is not, by itself, proof of compromise, maliciousness, detection validity, or a response decision.

Assign E001 to the supplied ticket/offense. Preserve source wording, raw values, original timestamps, and timezone information. Record missing or ambiguous data explicitly, including raw payload, event time, timezone, entity context, direction, port/protocol, log source, event/QID, and prior checks where material.

Distinguish:

- FACT: directly present in named evidence;
- OBSERVATION: a limited pattern or inconsistency in facts;
- HYPOTHESIS: a possible explanation that is not a fact;
- MISSING EVIDENCE: the narrowest information needed to test a material hypothesis.

Do not decode, enrich, normalize, or silently repair data at triage. Escalate raw-event interpretation to security-event-analysis.
