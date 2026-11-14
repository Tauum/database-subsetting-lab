-- Connect to poc_subset. Compare columns rather than changing database connections.
SELECT raw.id,
       raw.applicant_name AS original_name,
       safe.applicant_name AS masked_name
FROM public.application raw JOIN masked.application safe USING (id);

SELECT raw.id,
       raw.email AS original_email,
       safe.email AS masked_email,
       t.state->>'assignee' AS same_email_in_task_json,
       m.metadata->>'ownerEmail' AS same_email_in_metadata_json
FROM public.participant raw JOIN masked.participant safe USING (id)
JOIN masked.application a ON a.id=safe.application_id
JOIN masked.task t ON t.process_id=a.process_id
JOIN masked.document d ON d.participant_id=safe.id
JOIN masked.attachment attachment ON attachment.document_id=d.id
JOIN masked.attachment_metadata m ON m.attachment_id=attachment.id;

SELECT raw.id, raw.state AS original_defect, safe.state AS preserved_defect,
       (raw.state-'personalDetails')=(safe.state-'personalDetails') AS defect_fields_unchanged
FROM public.process_instance raw JOIN masked.process_instance safe USING (id);

-- Added JSON personal-data example: all values here are fabricated.
SELECT raw.id,
       raw.state->'personalDetails' AS original_personal_json,
       safe.state->'personalDetails' AS masked_personal_json,
       safe.state->>'submittedDate' AS preserved_malformed_date
FROM public.process_instance raw JOIN masked.process_instance safe USING (id);
