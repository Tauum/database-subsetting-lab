-- Run this in either IntelliJ data source. Source has 1001 and 1002; subset has 1001.
SELECT current_database() AS database, id AS process_id, state
FROM public.process_instance
ORDER BY id;

-- Defect, JSON reference, and logical orphan:
SELECT current_database() AS database,
       state->>'submittedDate' AS submitted_date,
       state->>'embeddedParticipantId' AS participant_reference
FROM public.process_instance WHERE id = 1001;

SELECT * FROM public.external_reference ORDER BY id;
SELECT * FROM public.process_instance_history ORDER BY id;
