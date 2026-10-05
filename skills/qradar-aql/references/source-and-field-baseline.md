# Source and field baseline

## SOURCE FACT

IBM documents AQL SELECT queries against Ariel events and flows, WHERE filtering, and START/STOP time criteria. For this Phase-1 skill, only QRadar Events are in scope. IBM documentation also describes custom event and flow properties, whose deployed names and availability are environment-specific.

## Conservative baseline

Use only these baseline fields/functions when the supplied request needs them: starttime, sourceip, destinationip, sourceport, destinationport, username, qid, logsourceid, payload, QIDNAME(qid), and LOGSOURCENAME(logsourceid).

This is a documented interoperability baseline, not proof that a particular QRadar deployment has the fields, data quality, permissions, timezone interpretation, custom properties, or query performance required by a request.

## Local mapping rule

Do not infer a Custom Event Property name from a requested concept. If command line is requested but its mapping is unknown, report the concept as unresolved and request its exact local property mapping. Never put a placeholder such as <CUSTOM_PROPERTY:CommandLine> inside a SELECT clause, filter, or any AQL-looking code.

## Sources

- IBM QRadar AQL Query Structure: https://www.ibm.com/docs/en/qsip/7.5.0?topic=aql-query-structure
- IBM QRadar Time Criteria in AQL Queries: https://www.ibm.com/docs/en/qradar-on-cloud?topic=language-time-criteria-in-aql-queries
- IBM QRadar Custom Event and Flow Properties: https://www.ibm.com/docs/en/qradar-on-cloud?topic=siem-custom-event-flow-properties
