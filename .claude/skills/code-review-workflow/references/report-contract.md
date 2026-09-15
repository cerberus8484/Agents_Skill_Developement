# Review report contract

FRAMEWORK INTERPRETATION, not a legal or normative report format.

## Scope

Record revision, reviewed paths, intended behavior, available evidence and exclusions. Record skills/references actually read, not merely offered by the host. Separate supplied test results from independently recorded harness checks (this reviewer does not execute). Attribute executor, command, revision and scope when available; missing provenance stays explicit. Record snapshot versus diff review and unknown baseline.

## Finding

- ID: stable R001 etc.; preserve any upstream evidence identifiers.
- Observation: concrete behavior and exact location.
- Evidence: source/revision; preconditions; counterevidence and unknowns.
- Layer and reachability: direct function / service / endpoint; input owner and guard evidence; CONFIRMED_PATH, GUARD_BLOCKS_PATH or PATH_UNKNOWN. A synthetic probe is not live-system evidence.
- Finding kind: BEHAVIORAL_DEFECT, INTERNAL_ROBUSTNESS, SECURITY_RISK or OPTIONAL_IMPROVEMENT; independent of priority.
- Impact and priority: contextual HIGH / MEDIUM / LOW; OPTIONAL for preference. No automatic CVSS.
- Confidence: HIGH / MEDIUM / LOW with reason, independent of priority.
- Recommendation: smallest effective change and its trade-off.
- Regression test: input, expected result and test layer; execution NOT_RUN unless attributable evidence exists.
- Mappings: list of framework, topic/verified identifier, source/version, rationale and status.
- Mapping status: SUPPORTED_TOPIC | VERIFIED_REFERENCE | CONTEXT_REQUIRED | SOURCE_UNAVAILABLE. VERIFIED_REFERENCE means reference checked, not requirement fulfilled.
- Source label: LAW_TEXT | SUPERVISORY_GUIDANCE | STANDARD_SOURCE | FRAMEWORK_INTERPRETATION | TECHNICAL_RECOMMENDATION.
- Owner: developer, security owner, DPO/legal or ISMS owner.

Use a separate evidence-gap list for processing purposes, scope, selected controls, supplier assurance, training or operational records absent from the code.

## Example (synthetic)

R001: a supplied handler logs a whole synthetic request body containing an email field. Record the actual logging call; whether production enables that level, retention and access restrictions are unknown. Recommend field allowlisting and a negative test asserting omitted sensitive fields. Attach GDPR relevance only with facts; an ISO topic remains CONTEXT_REQUIRED without the organization's selected requirement. Do not create three duplicate findings or claim a personal-data breach occurred.
