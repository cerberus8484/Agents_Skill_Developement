# Nexora Agents & Nexora Skills

**Nexora Agents** ist ein versionierbares, evidenzbasiertes Agenten-Framework für SOC, SIEM, Enterprise-IT und regulierte Entwicklungsumgebungen. **Nexora Skills** liefert die wiederverwendbaren Untersuchungs-, Review- und Engineering-Methoden. GitHub Copilot wird strukturell unterstützt; Codex und Claude Code sind bewusst noch als ungetestete Adapter dokumentiert.

> SIEM/SOC ist eine Fachdomäne des Frameworks – nicht dessen alleiniger Zweck.

## Einstieg

| Ziel | Einstieg |
|---|---|
| Framework verstehen | [Framework Foundation](framework/README.md) |
| IT-/SOC-Agenten nutzen und vergleichen | [Team-Handbuch und Runtime-Testplan](docs/it-soc-team.md) |
| Nexora Agent Bench ausführen | [Benchmark-Dokumentation](benchmarks/README.md) |
| Agent-Rechte und Adapter prüfen | [Nexora Agent Shield](docs/agent-shield.md) |
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
- **Nexora Agent Bench**: aktive deterministische Vertrags- und Konsistenzprüfung mit synthetischen SOC-Fällen.
- **Nexora Agent Shield**: aktive statische Prüfung von Agent-Rechten, Adapterkonfiguration und Daten-/Sicherheitsklauseln.

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
| Nexora Agent Bench | ACTIVE_OFFLINE – Schema-, Entscheidungs- und semantische Konsistenzprüfung |
| Nexora Agent Shield | ACTIVE_STATIC – Least-Privilege-, Adapter- und Vertragsprüfung |
| GitHub Copilot | STRUCTURAL_ONLY |
| OpenAI Codex | **READY** – 10/10 agents, 15/15 skills, 16/16 installer/schema checks and 87/87 repository tests validated with synthetic data on Windows |
| Claude Code | UNTESTED |

Die Plattformstatus sind keine Runtime-Freigaben. Details: [Adapter-Dokumentation](framework/adapters/).

`READY` gilt für die nachgewiesene Codex-Integration mit synthetischen Daten. Es ist keine Freigabe für Kundendaten, Produktionssysteme oder ungeprüfte externe Toolzugriffe. Nachweis: [Codex Runtime Validation](docs/codex-runtime-validation.md).

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
    python tools/sync_agents.py --check
    python tools/run_agent_shield.py
    python -m unittest
    python tools/run_benchmark.py --suite benchmarks/cases --responses benchmarks/fixtures/baseline

Für eine sichere, benutzerweite Codex-Installation unter Windows oder einem anderen lokalen System:

    python tools/sync_skills.py --prune
    python tools/sync_agents.py
    python tools/install_codex.py --dry-run
    python tools/install_codex.py

Der Installer sichert gleichnamige Nexora-Pakete, ersetzt nur diese vollständig und lässt fremde persönliche Skills und Agenten unverändert. Codex danach vollständig neu starten.

Der Skill-Sync erzeugt die drei Plattformfassungen aus kanonischen Quellen. Team-Agenten werden separat mit `python tools/sync_agents.py` synchronisiert; `--check` prüft sie ohne Änderungen. Nexora Agent Shield vergleicht Rechte und Adapter mit der expliziten Least-Privilege-Policy. Die Tests prüfen Dateiverträge und Synchronität, nicht native Plattform-Laufzeitwirkung. Nexora Agent Bench prüft zusätzlich den strukturierten Entscheidungsvertrag und deterministische Widersprüche, aber keine echte Toolaktivität.

## Beitrag leisten

1. Fachlichen Referenzrahmen und Primärquellen prüfen.
2. Nur eine kanonische Skill-Quelle unter framework/skills ändern.
3. Adapter generieren und Tests ausführen.
4. Plattformstatus nur anhand tatsächlicher Runtime-Nachweise anheben.

Der verbindliche Ablauf steht im [Skill-Review-Standard](docs/skill-review-standard.html).
