# Source baseline — checked 2026-09-15

## LAW_TEXT: German technical baseline

[BSIG § 30](https://www.gesetze-im-internet.de/bsig_2025/__30.html) was retrieved. It addresses risk-based technical and organizational measures for covered entities. Topic routing for a German review:
- paragraph 2 no. 4: supply-chain security;
- no. 5: acquisition/development/maintenance and vulnerability handling;
- no. 6: effectiveness assessment;
- no. 8: cryptographic practices;
- no. 9: access-control topics.
Paragraph 3 identifies priority for specified EU implementing requirements for specified service categories. Verify sector context rather than treating this table as exhaustive.

## EU baseline and access limit

[NIS2 Directive (EU) 2022/2555](https://eur-lex.europa.eu/eli/dir/2022/2555/oj/eng) is the primary EU reference. Its full text could not be extracted during this review; do not claim paragraph-by-paragraph EU verification from this baseline. Germany-specific mapping above is grounded in the retrieved national text. Verify current EU and jurisdiction-specific instruments before a legal mapping.

## FRAMEWORK_INTERPRETATION

A dependency-integrity gap may relate to supply-chain risk. Missing failure-path tests may relate to effectiveness assessment. These are conditional engineering connections, not proof of noncompliance. No direct equivalence to GDPR or ISO controls is asserted.

## TECHNICAL_RECOMMENDATION

For a concrete finding request relevant evidence from the security owner: implemented control, responsible owner and effectiveness record. Do not collect whole organizational repositories or personal records merely to complete a code review.
