# AQL Field Baseline

This baseline intentionally contains only QRadar event fields and functions documented by IBM for conservative Phase 1.3 queries:

- `starttime`, `sourceip`, `destinationip`, `sourceport`, `destinationport`
- `username`, `qid`, `logsourceid`, `payload`
- `QIDNAME(qid)` and `LOGSOURCENAME(logsourceid)` for returned labels

`hostname`, command line, parent process, process name, domain, hash, and URL are not assumed to be standard fields. They require the exact deployed Custom Event Property name and must be emitted as `<CUSTOM_PROPERTY:...>` placeholders until an analyst supplies it.

Query construction uses `FROM events` only in this phase. Use `START '…' STOP '…'` with the analyst-provided window without changing its meaning. Verify the QRadar console timezone before manually executing a request whose supplied times include a timezone offset.

Sources: IBM's [event fields reference](https://www.ibm.com/docs/en/qradar-on-cloud?topic=language-event-flow-simarc-fields-aql-queries), [AQL operators](https://www.ibm.com/docs/SS42VS_latest/com.ibm.qradar.doc/r_aql_operators.html), and [query structure](https://www.ibm.com/docs/en/qsip/7.5.0?topic=aql-query-structure).
