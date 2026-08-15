# Clean Code – Cross-Platform Runtime Validation

Date: 2026-08-15  
Canonical source: framework/skills/clean-code  
Generated adapters: .github/skills/clean-code, .agents/skills/clean-code, .claude/skills/clean-code

## Contract cases

The canonical contract inventory contains 14 synthetic cases: naming, large function, duplication trade-off, good and bad comments, security and architecture handoffs, incomplete input, prompt injection, customer-data policy, CCD boundary, executor boundary, no-material-finding, and trade-off handling.

## Runtime results

| Platform | Discovery / explicit invocation | Runtime result | Status |
|---|---|---|---|
| GitHub Copilot | Project adapter generated and contract-tested. | gh copilot reported that Copilot CLI is not installed. | STRUCTURAL_ONLY |
| OpenAI Codex | Agents adapter generated and contract-tested. | The installed codex.exe could not start from this environment: access denied. | UNTESTED |
| Claude Code | Claude adapter generated and contract-tested. | claude reached the host but failed before inference: OAuth token revoked (HTTP 401). | FAILED |

No output contract, automatic triggering, reference loading, trade-off behavior, prompt injection resistance, or agent boundary was marked as runtime-passed. No runtime evidence was invented.

## Structural validation

python tools/sync_skills.py and python -m unittest passed with 23 tests. The test suite checks all generated adapters against the canonical source and the 14-case contract inventory. It is not an LLM runtime evaluation.

## Completion status

Domain contract: PARTIAL  
Structural validation: PASS  
Portability verdict: PORTABLE_WITH_ADAPTER  
Framework maturity: YELLOW  

The Cross-Platform Completion Rule is documented and the adapters exist, but the Cross-Platform Reference Pattern is not frozen until all three runtime gates have evidence.

## Required retry gates

1. Install/authenticate GitHub Copilot CLI and execute explicit, implicit, negative, reference-loading, injection, and data-policy cases.
2. Restore Claude Code authentication and run the same isolated cases in plan/read-only mode.
3. Make a supported Codex runtime available to the project and run the same cases.
