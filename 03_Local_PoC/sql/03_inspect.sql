SELECT id, organisation_id, state FROM process_instance ORDER BY id;
SELECT * FROM external_reference ORDER BY id;
SELECT 'domain' AS kind, count(*) FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE '%_history'
UNION ALL
SELECT 'history',count(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE '%_history';
