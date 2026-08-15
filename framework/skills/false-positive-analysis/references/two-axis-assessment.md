# Two-axis assessment

## SOURCE FACT

NIST describes incident handling as a process that incorporates analysis, containment, eradication, recovery, and post-incident activity. A bounded assessment is therefore not a production authorization or a closure decision. See NIST SP 800-61 Rev. 3.

MITRE ATT&CK detection content uses locally adaptable context and exceptions to improve detection logic. It does not make a known tool, account, or exception a universal proof of legitimacy or maliciousness.

## FRAMEWORK INTERPRETATION

Keep two questions independent:

1. Did the documented detection condition occur?
2. What, if anything, does the supplied evidence support about the activity?

The detection-validity answer does not imply the activity answer. A technically true detection can represent approved activity. Legitimate activity does not prove a false detection.

## OUR RECOMMENDATION

Return both classifications, their confidence, supporting and contradicting evidence, data-quality concerns, and the smallest missing evidence to the investigation owner.
