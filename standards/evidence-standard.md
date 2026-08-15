# Evidence Standard

## Evidence is immutable input

Evidence is any analyst-provided source: ticket data, event export, raw log, query result, CSV, JSON, screenshot transcription, or investigation note. Store it without silently correcting, normalizing, redacting, or altering its source timestamp.

## Minimum evidence record

Each record has an ID, type, source, title, received timestamp, original content or a stable raw reference, and extracted facts. Use `schemas/evidence.schema.json`.

## Attribution rules

- A fact must name at least one evidence ID.
- Extraction may make a field explicit, but must not introduce a value absent from the source.
- If a parsed field conflicts with the raw payload, preserve both and record the inconsistency as an observation.
- Times retain the original value and timezone. If a timezone is absent, record that it is absent; do not assume one.
- Mark analyst claims as `analyst_note`; they are evidence of the claim, not independent verification.

## Evidence quality

Record gaps that affect interpretation: missing raw payload, incomplete time window, unknown log source, parsing failure, truncated export, unknown timezone, or missing entity context.
