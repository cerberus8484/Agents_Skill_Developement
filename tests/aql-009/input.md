# Synthetic QUERY REQUEST: Locally validated baseline

Purpose: Review events for exact user LAB\a.smith.
Data Source: QRadar Events
Entity: User LAB\a.smith (exact match)
Time Window: 2026-08-14 09:00:00Z to 2026-08-14 09:30:00Z
Required Fields: timestamp, username, source IP, destination IP, QID, log source
Reason: Evaluate H009.

Local validation evidence: Analyst record V001, QRadar 7.5 test environment, validated 2026-08-15; exact baseline fields and UTC time interpretation were syntax-tested successfully. No execution authorization was supplied.
