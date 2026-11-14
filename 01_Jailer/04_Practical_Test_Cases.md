# Jailer hands-on checks
- Run extraction from process_instance 1001 using generated FK associations; count rows and note unrelated process 1002.
- Restrict traversal to avoid sibling process, then rerun.
- Add logical associations for process_instance_history and external_reference.
- Explicitly extract orphan external_reference 11002 as a separate subject; it is unreachable from process 1001.
- Inspect JSONB embedded participant ID manually and preserve malformed date.
- Import resulting INSERT SQL into fresh schema; run `tests/check_subset.sql`.
- Record model-editing time, output size, rows, duration and errors.
Jailer is not a substitute for privacy review. Never send real personal data into a local trial.
