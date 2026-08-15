# AQL Field Baseline

This baseline intentionally contains only QRadar event fields and functions documented by IBM for conservative Phase 1.3 queries:

- `starttime`, `sourceip`, `destinationip`, `sourceport`, `destinationport`
- `username`, `qid`, `logsourceid`, `payload`
- `QIDNAME(qid)` and `LOGSOURCENAME(logsourceid)` for returned labels

`hostname`, command line, parent process, process name, domain, hash, and URL are not assumed to be standard fields. They require the exact deployed Custom Event Property name. Until an analyst supplies a traceable local mapping, report the field as unresolved and produce no AQL statement that contains a placeholder or guessed property name.

Query construction uses `FROM events` only in this phase. Use `START '…' STOP '…'` with the analyst-provided window without changing its meaning. Verify the QRadar console timezone before manually executing a request whose supplied times include a timezone offset.

The documented baseline and IBM examples do not establish that a field, its semantics, timezone interpretation, permissions, or query behavior is valid in a particular local QRadar deployment. Local validation is separate from authorization to execute.

Sources: IBM's [event fields reference](https://www.ibm.com/docs/en/qradar-on-cloud?topic=language-event-flow-simarc-fields-aql-queries), [AQL operators](https://www.ibm.com/docs/SS42VS_latest/com.ibm.qradar.doc/r_aql_operators.html), [time criteria](https://www.ibm.com/docs/en/qradar-on-cloud?topic=language-time-criteria-in-aql-queries), and [query structure](https://www.ibm.com/docs/en/qsip/7.5.0?topic=aql-query-structure).
