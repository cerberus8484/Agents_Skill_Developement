# Canonical Agent & Skill Framework

framework/ is the source of truth for framework-owned skills, references, policies, agent data models, and platform adapter specifications. Existing .github/skills SIEM skills remain legacy compatibility artefacts until individually migrated.

## Core distinctions

| Term | Meaning |
|---|---|
| DOMAIN / REFERENCE | Fachliche Grundlage; not automatically executable. |
| SKILL | Reusable, invokable method. |
| AGENT | Role that uses skills. |
| TOOL | Technical mechanism. |
| CAPABILITY | What an artefact can do. |
| PERMISSION | What a runtime authorizes in a concrete environment. |
| POLICY | Binding framework rule. |
| PLATFORM ADAPTER | Generated or documented platform-specific delivery. |

Capability is not permission. A skill is not an agent. A reference is not automatically a skill.

## Source-of-truth strategy

Each framework-owned skill has one editable canonical directory under framework/skills/name. tools/sync_skills.py generates identical adapters under .github/skills/name, .agents/skills/name, and .claude/skills/name; do not edit generated files manually. Adapter presence is structural preparation, not runtime validation.

Every changed framework-owned skill or agent follows the Cross-Platform Completion Rule: GitHub Copilot, OpenAI Codex, and Claude Code must each be considered, receive a documented adapter or explicit integration decision, and carry separate status.

## Cross-Platform Completion Rule

A skill or agent is not fully processed until its fachlicher Review, capability and limitation contract, security/data-policy references, canonical source, three platform decisions, contract tests, platform status, and documentation are present. Runtime validation is never inferred from file structure.

## Honesty labels

Use BELEGT, PRAXISBEWÄHRT, FRAMEWORK_AUSSAGE, INTERPRETATION, EMPFEHLUNG, and UNSICHER. Keep source fact, framework interpretation, and recommendation separate.
