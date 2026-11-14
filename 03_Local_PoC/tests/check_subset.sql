-- Run against a restored SUBSET database, not the source. Override expected counts as necessary.
DO $$
BEGIN
 IF NOT EXISTS(SELECT 1 FROM process_instance WHERE id=1001) THEN RAISE EXCEPTION 'Missing target'; END IF;
 IF EXISTS(SELECT 1 FROM process_instance WHERE id=1002) THEN RAISE EXCEPTION 'Unrelated sibling included'; END IF;
 IF NOT EXISTS(SELECT 1 FROM application WHERE process_id=1001) THEN RAISE EXCEPTION 'Missing application'; END IF;
 IF NOT EXISTS(SELECT 1 FROM process_instance_history WHERE record_id=1001) THEN RAISE EXCEPTION 'Missing history'; END IF;
 IF (SELECT state->>'submittedDate' FROM process_instance WHERE id=1001) <> '31/99/2026' THEN RAISE EXCEPTION 'Defect changed'; END IF;
END $$;
