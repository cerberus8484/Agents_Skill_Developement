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

Each framework-owned skill has one editable canonical directory under framework/skills/name. tools/sync_skills.py generates the GitHub Copilot adapter under .github/skills/name; do not edit generated files manually.

No Codex or Claude Code adapter is generated yet: their project-level discovery contract was not established by the evidence collected for this repository. Their status is UNTESTED, not inferred.

## Honesty labels

Use BELEGT, PRAXISBEWÄHRT, FRAMEWORK_AUSSAGE, INTERPRETATION, EMPFEHLUNG, and UNSICHER. Keep source fact, framework interpretation, and recommendation separate.
