-- Expected source rows; compare with exports, never treat these as automatic extraction rules.
SELECT 'process_instance', count(*) FROM process_instance WHERE id=1001;
SELECT 'application', count(*) FROM application WHERE process_id=1001;
SELECT 'participant',count(*) FROM participant WHERE application_id IN (SELECT id FROM application WHERE process_id=1001);
SELECT 'history',count(*) FROM process_instance_history WHERE record_id=1001;
SELECT 'logical_reference',count(*) FROM external_reference WHERE parent_process_id=1001;
SELECT 'orphan',count(*) FROM external_reference WHERE parent_process_id=999999;
