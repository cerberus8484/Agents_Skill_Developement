# Phase 1.3: QRadar AQL Validation

## Scope

`qradar-aql` translates one analyst-provided, structured `QUERY REQUEST` from `qradar-investigation` into a minimal, read-only QRadar AQL **event** query. It explains purpose, filters, preserved time window, returned fields, assumptions, expected analyst return data, and limitations. It does not execute the query.

## New and changed files

- Added `.github/skills/qradar-aql/SKILL.md`.
- Added `knowledge/qradar/aql-field-baseline.md` with the documented field baseline and source links.
- Added `tests/test_aql_fixtures.py` and `tests/aql-001` through `tests/aql-008`.
- Updated the repository and test READMEs to use the complete test command.

## Supported query types

- Host searches through an analyst-confirmed hostname Custom Event Property.
- Exact user, source IP, destination IP, and any-direction IP event searches.
- Numeric QID and numeric log-source-ID event searches.
- Authentication and network event searches using known standard fields.
- Process and IOC investigations through a safe base query plus explicitly replaceable Custom Event Property placeholders.

Flows are deliberately not generated in Phase 1.3. A request for flows is rejected or deferred rather than mixed with `events`.

## Tested AQL patterns

The eight synthetic fixtures test a host custom property, exact user, source IP, source/destination `OR`, numeric QID, unknown process command-line property, missing time window, and a rule-change request alongside a valid query request.

Run all Phase 1 tests:

```powershell
python -m unittest
```

## Custom properties and safety

Only QRadar fields documented in `knowledge/qradar/aql-field-baseline.md` are treated as known. Hostname, command line, parent process, process, domain, hash, and URL remain quoted `<CUSTOM_PROPERTY:...>` placeholders until the analyst supplies their exact local name.

The skill rejects missing time constraints, never invents a QID or property name, preserves supplied time-window meaning, uses `FROM events` only, excludes `SELECT *`, and rejects rule/configuration changes, query execution, API access, SSH, and Jumpserver automation.

## Known limits and open points

This is a prompt skill, so automated tests validate fixture completeness and stated safety boundaries, not the parser or execution of a generated AQL query. Analysts must manually run the eight fixtures through Copilot and validate the generated query in their approved QRadar environment. QRadar console timezone behavior, deployed Custom Event Property names, local log-source IDs, and exact event-field availability require environment-specific confirmation.

## Recommended next step

Perform the manual AQL regressions and capture any syntax or field-mapping corrections in `knowledge/qradar/`. Then implement `security-event-analysis`, reusing the same evidence IDs and keeping raw-event parsing separate from query generation.
