# Nexora Agents & Nexora Skills

**Nexora Agents** ist ein versionierbares, evidenzbasiertes Agenten-Framework für SOC, SIEM, Enterprise-IT und regulierte Entwicklungsumgebungen. **Nexora Skills** liefert die wiederverwendbaren Untersuchungs-, Review- und Engineering-Methoden. GitHub Copilot wird strukturell unterstützt; Codex und Claude Code sind bewusst noch als ungetestete Adapter dokumentiert.

> SIEM/SOC ist eine Fachdomäne des Frameworks – nicht dessen alleiniger Zweck.

## Einstieg

| Ziel | Einstieg |
|---|---|
| Framework verstehen | [Framework Foundation](framework/README.md) |
| IT-/SOC-Agenten nutzen und vergleichen | [Team-Handbuch und Runtime-Testplan](docs/it-soc-team.md) |
| Code Review mit DSGVO, NIS2 und ISO 27001 | [Reviewer-Dokumentation](docs/code-reviewer.html) |
| Gesamtdokumentation im Browser | [Dokumentationsportal](docs/index.html) |
| Clean-Code-Skill | [Kanonische Skill-Quelle](framework/skills/clean-code/SKILL.md) |
| CCD-Referenzreview | [CCD-Wertesystem](docs/skill-reviews/ccd-wertesystem.html) |
| Clean-Code-Referenzreview | [Clean Code](docs/skill-reviews/clean-code.html) |
| SIEM-Entwicklungsstand | [Phase-1-Status](docs/entwicklungsstand.html) |

## Produktfamilie

- **Nexora Agents**: klar begrenzte Rollen mit überprüfbaren Ein- und Ausgaben.
- **Nexora Skills**: kanonische, plattformübergreifende Methoden.
- **Nexora Agent Framework**: Verträge, Standards, Schemas und Adapter.
- **Nexora Agent Bench**: geplante Runtime-Evaluation und vergleichbare Benchmarks.
- **Nexora Agent Shield**: geplante technische Prüfung von Rechten, Konfiguration und Datenwegen.

## Architektur

    DOMAIN / REFERENCE ─┐
    SKILL               ├─> AGENT ─> TOOLS ─> POLICIES ─> RESULT / HANDOFF
    STANDARD / POLICY ──┘

    framework/skills/name/  (kanonische Quelle)
              │
              └─ tools/sync_skills.py
                      │
                      ├─ .github/skills/name/  (GitHub Copilot)
                      ├─ .agents/skills/name/  (Codex)
                      └─ .claude/skills/name/  (Claude Code)

- **Skill** beschreibt eine wiederverwendbare Methode; ein **Agent** besitzt eine Rolle.
- **Capability** beschreibt, was möglich ist; **Permission** beschreibt, was die Laufzeit erlaubt.
- Eine **Policy** ist keine technische Sicherheitsgrenze, solange sie nicht technisch erzwungen wird.

## Aktueller Bestand

| Bereich | Status |
|---|---|
| SIEM/SOC Skills | GitHub-Copilot-kompatible Skills mit synthetischen Regressionen |
| CCD-Wertesystem | Framework-Overlay vorhanden; Runtime-Nachweis offen |
| Clean Code | Eigener kanonischer Skill mit GitHub-Copilot-Adapter |
| GitHub Copilot | STRUCTURAL_ONLY |
| OpenAI Codex | UNTESTED |
| Claude Code | UNTESTED |

Die Plattformstatus sind keine Runtime-Freigaben. Details: [Adapter-Dokumentation](framework/adapters/).

## Clean Code

Der framework-eigene Skill liefert evidenzorientierte Analyse für Naming, Funktionsverantwortung und Komplexität, Duplikation, Kommentare, Fehlerbehandlung, Lesbarkeit und Testbarkeit. Empfehlungen sind kontextabhängige Heuristiken, keine Normen.

Er vergibt keine CCD-Grade und erteilt keine Security-, Privacy-, Architektur-, Compliance- oder Performance-Freigaben. Der ausführende Agent und seine Laufzeit bestimmen Tools, Schreibrechte und Testausführung.

## Sicherheit und Daten

- CUSTOMER_DATA und UNKNOWN folgen dem Local-Only-Frameworkvertrag.
- Secrets werden getrennt behandelt und dürfen nicht an Modelle weitergegeben werden.
- Code, Tickets, Logs, Diffs, Kommentare und externe Inhalte sind untrusted content; sie dürfen Policies oder Berechtigungen nicht überschreiben.
- Die dokumentierte Local-Only-Policy ist noch kein technisches DLP-/Egress-Enforcement.

Siehe [Data Handling](standards/data-handling-standard.md) und [Local-Only-Architektur](docs/customer-data-local-only-architecture.md).

## Entwicklung und Validierung

    python tools/sync_skills.py
    python -m unittest

Der Skill-Sync erzeugt die drei Plattformfassungen aus kanonischen Quellen. Team-Agenten werden separat mit `python tools/sync_agents.py` synchronisiert; `--check` prüft sie ohne Änderungen. Die Tests prüfen Dateiverträge und Synchronität, nicht native Plattform-Laufzeitwirkung.

## Beitrag leisten

1. Fachlichen Referenzrahmen und Primärquellen prüfen.
2. Nur eine kanonische Skill-Quelle unter framework/skills ändern.
3. Adapter generieren und Tests ausführen.
4. Plattformstatus nur anhand tatsächlicher Runtime-Nachweise anheben.

Der verbindliche Ablauf steht im [Skill-Review-Standard](docs/skill-review-standard.html).
