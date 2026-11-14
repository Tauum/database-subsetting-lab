# Tonic Structural: limits and tests

## Strengths to assess
- Consistent masking across related records
- Subsetting based on root conditions
- JSON/JSONB field transformations
- Repeatable scheduled jobs and available API controls

## Risks
- Masking could repair the malformed date and destroy the bug.
- Relationship-preserving selection could omit deliberately orphaned logical records.
- Some transformations may alter key or type semantics.
- Destination database, licensing and network access may be required.
- Cloud trials must use fabricated data unless explicitly approved.

## Evaluation questions
1. Can a root record ID be changed automatically per job?
2. Can missing/virtual relationships be configured?
3. Can a malformed JSON string be preserved verbatim?
4. Can a logically orphaned row be included by an explicit root/selection rule?
5. Does the product produce SQL or backups directly, or only a destination database?
6. Can masked outputs be inspected before release?
7. What telemetry leaves self-hosted deployment?
8. How are source row counts and query costs bounded?
9. How much operator setup is required for a new defect?
10. Does the available trial include the necessary features?
