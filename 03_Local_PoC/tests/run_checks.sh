#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "Checking 24 tables, deep chain, malformed JSON and logical orphan..."
docker compose exec -T db psql -U poc -d poc -v ON_ERROR_STOP=1 <<'SQL'
DO $$
DECLARE n int;
BEGIN
 SELECT count(*) INTO n FROM information_schema.tables WHERE table_schema='public';
 IF n <> 24 THEN RAISE EXCEPTION 'Expected 24 tables, got %', n; END IF;
 IF NOT EXISTS (SELECT 1 FROM attachment_metadata m JOIN attachment a ON a.id=m.attachment_id JOIN document d ON d.id=a.document_id JOIN participant p ON p.id=d.participant_id JOIN application ap ON ap.id=p.application_id JOIN process_instance pi ON pi.id=ap.process_id WHERE pi.id=1001) THEN
   RAISE EXCEPTION 'Deep chain missing';
 END IF;
 IF (SELECT state->>'submittedDate' FROM process_instance WHERE id=1001) <> '31/99/2026' THEN
   RAISE EXCEPTION 'Malformed date missing';
 END IF;
 IF NOT EXISTS (SELECT 1 FROM external_reference er LEFT JOIN process_instance p ON p.id=er.parent_process_id WHERE p.id IS NULL) THEN
   RAISE EXCEPTION 'Logical orphan missing';
 END IF;
 IF NOT EXISTS (SELECT 1 FROM process_instance WHERE id=1002 AND organisation_id=1) THEN
   RAISE EXCEPTION 'Unrelated sibling missing';
 END IF;
 RAISE NOTICE 'All source fixture assertions passed';
END $$;
SQL
