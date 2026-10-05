# ATT&CK and analyst handoff

**SOURCE FACT:** MITRE ATT&CK describes adversary techniques, data sources, detection strategies, and analytics. It does not endorse a specific SIEM vendor implementation.

Use ATT&CK technique and sub-technique identifiers as traceable behaviour vocabulary. For every mapping, state whether it is directly evidenced, inferred from a detection hypothesis, or only a proposed coverage target. Do not map a generic tool name or a single event to attacker intent.

**SOURCE FACT:** NIST incident-response guidance places containment within organization-specific response criteria and procedures. Detection evidence and a hunt result do not independently authorize operational action.

Safe handoff must name:

- the evidence and data-quality limitations;
- the hunt/rule version, backend, and query status;
- matched conditions and contradictory or legitimate-context evidence;
- confidence rationale and unresolved gaps;
- the accountable analyst or incident-response role for the next decision.
