# Time and correlation

## Time axes

Keep each named source time distinct:

- Device/event time: reported by the originating device or event.
- SIEM receive time: reported as received by the SIEM.
- SIEM stored/start time: reported by the SIEM storage or query result.
- Analyst-provided time: stated in analyst context.

Do not silently convert timezones or decide which clock is correct. State absent timezone and material discrepancies as evidence-quality gaps.

## Relationship labels

- Exact duplicate: supplied records are identical; preserve both.
- Related: supplied records share an entity, bounded time interval, or other stated link.
- Temporal relation: one record precedes another by a stated interval.
- Correlation: evidence supports a bounded association.

None of these labels proves causation. Require direct supplied linkage before asserting that a process initiated a network connection or that one event caused another.
