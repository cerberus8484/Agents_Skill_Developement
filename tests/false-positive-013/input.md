# Raw/parsed conflict with contextual legitimacy indicators

- E001: Parser output says `process=powershell.exe` and is the asserted detection condition.
- E002: Preserved raw event says `process=notepad.exe` for the same event identifier.
- E003: The parsed process is signed by Microsoft and used by an administrator account.
- F001: security-event-analysis recorded `DATA_QUALITY: raw/parsed process mismatch` without identifying a cause.

No verified change record, exact command, independent process telemetry, or local parser validation is supplied.
