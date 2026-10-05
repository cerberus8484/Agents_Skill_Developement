# Meaningful regression review

FRAMEWORK INTERPRETATION / engineering heuristics, not a standard or language-specific guarantee.

- Success path: assert observable output or durable effect, not just absence of exceptions.
- Error path: assert error contract and absence of forbidden side effects.
- Authorization: owner, different user, no identity; test the server boundary rather than only a UI button.
- Sensitive logging: synthetic markers must not appear; also assert required non-sensitive diagnostics remain.
- Deletion: clarify intended data scope and failure semantics; a mocked database call does not prove deletion.
- Isolation: fixtures reset state, clocks are controlled when necessary, no production endpoints.
- Mock fidelity: an assertion on a stub returning its configured result does not test the production implementation.
- Results: confirm tests were discovered; check skips/xfails, revision and relevant test selection. An exit code alone is incomplete evidence.
- Schema validation: separate malformed definitions (unknown type, null schema) from invalid user values. Internal schema tests and request tests establish different properties.
- Layer: a direct-function probe does not prove endpoint reachability. Propose a separate entry-point test when earlier guards or transformations affect the result.
- Counterexample: preserve intentionally accepted conversion as a positive test if the contract allows it. Do not demand rejection without a requirement.
- Provenance: a harness run substantiates only its selected tests and revision, not native agent invocation or untested layers.

When missing a test harness, propose input and oracle in prose and label NOT_RUN. Do not invent language APIs or executable test code without project context.
