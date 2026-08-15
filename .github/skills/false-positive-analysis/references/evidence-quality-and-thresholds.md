# Evidence quality and thresholds

## SOURCE FACT

NIST SP 800-86 treats the integrity and handling of computer-security incident evidence as material to forensic integration. NIST SP 800-94 discusses IDPS and SIEM-style analysis, including the need to understand alert limitations and tune detection in an environment.

ATT&CK Detection Strategies document environment-specific tuning elements, such as user context and time windows. These are calibration inputs, not proof of a conclusion in another environment.

## FRAMEWORK INTERPRETATION

Evidence must remain attributable. Raw/parsed mismatches, missing timezones, uncertain identity mapping, duplicate records, incomplete collection, and conflicting change context are assessment inputs. They can prevent either a confirmed classification or a detection-validity conclusion.

A signed binary, administrator identity, known administrative tool, maintenance window, or suspicious utility is contextual evidence only. It cannot alone prove legitimate or malicious activity.

## OUR RECOMMENDATION

For each axis, list the direct support, direct contradiction, and decision-relevant gap. Prefer `UNDETERMINED` or `INCONCLUSIVE` to a stronger label when evidence quality is insufficient.
