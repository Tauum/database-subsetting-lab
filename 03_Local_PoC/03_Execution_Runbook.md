# Reproducible evaluation runbook
1. Start synthetic source; run `bash tests/run_checks.sh`.
2. Reset source before each tool; record tool version, connection settings and model revision.
3. Select `process_instance.id=1001`. Start with declared FK traversal; document missing history/JSON links.
4. Add explicit associations for `record_id`, `parent_process_id`, and JSON `embeddedParticipantId` where supported.
5. Export subset. For Tonic, if the evaluated edition requires a destination database, use a separate synthetic destination and export via pg_dump; record this as an infrastructure penalty.
6. Import SQL fixture to isolated `poc_subset` using `bash tests/restore_and_check.sh /absolute/path/subset.sql`. The check requires history and exclusion of sibling 1002.
7. Record results in evaluation scorecard; manually inspect the JSON and all free-text fields.
8. Repeat with scale generator, record durations, and monitor resource use. Do not infer production performance from local timings.
The supplied script accepts plain SQL INSERT-compatible fixtures only, not pg_dump custom format. For custom dumps use `pg_restore` after creating a matching empty target database.
