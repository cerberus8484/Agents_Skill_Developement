# Code Security Reviewer — Version 0.3

Stand: 2026-09-15. Für Veröffentlichung vorbereitet; der interne Detailbericht ist ausgeschlossen. Runtime-Nachweise bleiben separat.

## Update nach Nexora-Praxistest

Version 0.3 präzisiert code-review-workflow, security und test-review anhand des begrenzten internen Praxistests (Detailbericht bleibt lokal). Neu: Aufrufer-/Guard-Nachweis, Eingabeeigentümer, direkte Funktion gegenüber Endpunkt, getrennte Befundart und Priorität sowie positive Gegenbeispiele bei erlaubter Typkonvertierung.

Die Tool-Rechte bleiben unverändert. Lesender Zugriff über einen ausdrücklich autorisierten Test-Harness ist von Projektcode-Ausführung getrennt; der Agent erhält keine generelle Shell-Freigabe. Ohne erlaubten Zugriff fordert er Ausschnitte an.

Die sechs ergänzten manuellen Fälle 11–16 sind noch NOT_RUN. Alle 63 bestehenden Repositorytests sowie drei Skill-Validierungen sind erfolgreich; sie beweisen keine verbesserte Modellleistung. Keine unabhängige Neubewertung erfolgt. Runtime bleibt UNTESTED / YELLOW; Lint weiter offen. DSGVO, NIS2, ISO und Clean Code wurden in diesem Ausbau nicht geändert. Der Skill-Creator begrenzt die Anpassung auf beobachtete Schwächen, statt zusätzliche allgemeine Regeln einzubauen.

## Aufgaben und Zuordnung

Der Agent bleibt ein read-only Reviewer. Er untersucht konkrete Änderungen und Kontext, nicht pauschal die gesamte Organisation.

| Skill | Aufgabe | Status der Fachbasis |
|---|---|---|
| code-review-workflow (neu) | Scope, Gegenprüfung, deduplizierte Befunde und Re-Review | PRACTICE_BASED |
| clean-code (bestehend) | Wartbarkeit und kontextabhängige Qualitätsheuristiken | bestehender Review unverändert |
| security (bestehend) | Technische AppSec-Befunde, präzisierte Aufrufer-/Schema-Grenze | Fachbasis übernommen; neue Heuristik PRACTICE_BASED |
| test-review (neu) | Assertions, Negativfälle und Ergebnisnachweise | PRACTICE_BASED |
| dsgvo (bestehend) | Technische Datenschutzaspekte und rechtliche Übergaben | bestehender Review unverändert |
| nis2-technical-review (neu) | Bedingte Zuordnung technischer Befunde zu Risikomanagementthemen | PARTIALLY_VERIFIED |
| iso27001-control-review (neu) | Vergleich mit belegten ausgewählten ISMS-Anforderungen | PARTIALLY_VERIFIED |

Die vier ursprünglich neuen Module sind eigene Framework-Arbeit; keine importierten Fremdskills, keine Skripte und keine allowed-tools-Deklaration. Letzteres bedeutet nicht, dass Skills grundsätzlich keine Tools deklarieren könnten. Der Agent wurde zunächst von 0.1 auf 0.2 und nach dem Nexora-Test auf 0.3 erweitert.

## Fachliche Grenze

DSGVO, NIS2 und ISO sind weder untereinander gleich noch durch Code allein vollständig prüfbar. Ein Risiko darf mehrere belegte Bezüge haben, bleibt aber ein Befund mit einer stabilen R-ID. Fehlende organisatorische Unterlagen sind Nachweislücken, nicht automatisch Kontrollversagen.

Beispiel: Eine synthetische Request-Logging-Funktion schreibt personenbezogene Felder. Der Reviewer nennt die Fundstelle, vermutete Auswirkungen und unbekannte Laufzeit-/Aufbewahrungseinstellungen. Er empfiehlt gezielte Feldfreigaben und einen Negativtest. Kein automatisches Urteil „Datenschutzverletzung“, kein dreifacher Befund für drei Frameworks.

Rechtliche Betroffenheit, Rechtsgrundlagen, DSFA und Meldungen: verantwortliche Rechts-/Datenschutzfunktion. ISMS-Anwendungsbereich, Kontrollauswahl und Risikoakzeptanz: ISMS-Verantwortliche. Änderungen: autorisierter Entwickler. Der Reviewer führt keine Tests oder Scans aus.

## Quellen und Zugriffslimits

- [§ 30 BSIG](https://www.gesetze-im-internet.de/bsig_2025/__30.html): deutscher Gesetzestext geprüft; technische Themenzuordnung im Skill. Keine pauschale Übertragung auf andere Länder.
- [NIS2 EU-Referenz](https://eur-lex.europa.eu/eli/dir/2022/2555/oj/eng): Volltext bei diesem Lauf nicht auslesbar. Kein vollständiger EU-Rechtsreview behauptet.
- [ISO 27001](https://www.iso.org/standard/27001) und [ISO 27002](https://www.iso.org/standard/75652.html): öffentliche Übersichten geprüft; kein lizenzierter Volltext und keine organisationsspezifische Kontrollauswahl vorhanden. Deshalb keine erfundenen Annex-A-Nummern.
- [EDPB Art. 25](https://www.edpb.europa.eu/documents/guideline/guidelines-42019-on-article-25-data-protection-by-design-and-by-default_en): offizielle Leitlinienseite geprüft; bestehender DSGVO-Skill wird weiterverwendet.

Gesetzestext, Aufsichtsleitlinie, Normquelle, Framework-Interpretation und technische Empfehlung werden im Bericht gekennzeichnet. Ein verifizierter Quellenverweis ist keine Bestätigung erfüllter Anforderungen.

## Bedienung

In einem freigegebenen Workspace den IT Code Security Reviewer wählen. Beispiel:

> Prüfe den bereitgestellten synthetischen Diff auf Korrektheit, Security, Testqualität und technische DSGVO-, NIS2- sowie ISO-27001-Bezüge. Keine Änderungen oder Befehle. Trenne belegte Probleme von offenen Nachweisen. ISMS-Scope und Rechtsbetroffenheit sind noch unbekannt.

Erwartet: Scope, Abdeckung pro Prüfbereich, priorisierte R-IDs mit Fundstelle und Gegenbelegen, gezielte Verbesserung und Regressionstest, getrennte Nachweislücken und Empfänger.

CUSTOMER_DATA und UNKNOWN bleiben LOCAL_ONLY. Vor dem Lesen muss der erlaubte Verarbeitungspfad geklärt sein. Lokal gespeicherte Dateien sind kein Beweis lokaler Inferenz.

## Cross-Platform und Pflege

Kanonisch: framework/agents/code-security-reviewer.md und framework/skills/<name>/SKILL.md. Agent-Metadaten: framework/agents/team.json.

Skill-Kopien: .github/skills, .agents/skills, .claude/skills. Agent-Adapter: .github/agents, .codex/agents, .claude/agents. Die bestehende Synchronisierung wurde um die vier Skills ergänzt. Im aktuellen Lauf wurden ausschließlich neue Skill-Verzeichnisse und die drei geänderten Reviewer-Adapter erzeugt; die bestehenden Fachskills blieben unverändert.

Copilot und Claude: read/search-basierte Tool-Listen. Codex: bestehendes TOML-Format; technische Hostbindung der Berechtigungen und Picker weiterhin unbestätigt. Kein globaler Installer aufgerufen.

## Nachweise und offene Arbeit

- 63 Repositorytests erfolgreich, einschließlich zwei neuer Paket-/Zuordnungstests.
- Vier Skill-Creator-Validierungen erfolgreich.
- Strukturtests prüfen Dateien, Referenzen und Synchronität, nicht Modellentscheidungen.
- Ruff fehlt in der verwendeten Python-Umgebung: Lint offen.
- Keine Runtime-Tests oder unabhängige Verhaltensvalidierung in diesem Lauf.
- Alle drei Plattformen: STRUCTURAL_ONLY / Runtime UNTESTED. Framework YELLOW.
- Testplan: [synthetische Review-Fälle](../tests/fixtures/code-review-runtime.md).

Qualitätskurzurteil: begrenzte Erweiterung mit wiederverwendetem DSGVO-/Security-Kern und expliziten Quellenlücken. Kein CCD-Grad vergeben; strukturelle Prüfungen sind keine vollständige Qualitätsbewertung. Als Nächstes Runtime-Fälle und Quellen-/Anwendbarkeitsnachweise prüfen; keine zusätzlichen Agents automatisch erzeugen.
