# Scenario catalogue and acceptance
1. Root process 1001: include required application, participant, document, attachment, task and approval records.
2. Shared organisation: avoid dragging unrelated process 1002 into export; configure association direction.
3. JSONB: preserve invalid `submittedDate=31/99/2026`; test `embeddedParticipantId=3001` explicitly.
4. Undeclared relation: `external_reference.parent_process_id` has no FK; add logical association manually.
5. Orphan: `parent_process_id=999999` is intentionally invalid; select explicitly, not via normal FK traversal.
6. History: record_id links are logical; add all needed history tables.
7. Masking: replace email/name/JSON ownerEmail while keeping stable join keys and malformed value.
8. Restore: load tool-produced SQL into fresh schema, run `tests/check_subset.sql`.
For each tool record configuration minutes, row counts per table, extracted bytes, duration, failed restores, defect reproduction, and privacy review findings. Tests 4 and 5 require custom configuration, not assumed automatic.
