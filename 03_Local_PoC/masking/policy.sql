-- Synthetic fixture policy v1. Runs inside the runner's transaction.
-- Helpers live only in this session and are not part of the masked schema.
CREATE FUNCTION pg_temp.email_token(value text) RETURNS text
LANGUAGE sql IMMUTABLE STRICT AS $$
 SELECT 'masked-' || md5(lower(btrim(value))) || '@example.invalid'
$$;

CREATE FUNCTION pg_temp.mask_json(value jsonb, field_name text DEFAULT '') RETURNS jsonb
LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE result jsonb; scalar text;
BEGIN
 IF value IS NULL THEN RETURN NULL; END IF;
 CASE jsonb_typeof(value)
 WHEN 'object' THEN
   SELECT coalesce(jsonb_object_agg(key, pg_temp.mask_json(v, key)), '{}'::jsonb)
   INTO result FROM jsonb_each(value) AS item(key, v);
   RETURN result;
 WHEN 'array' THEN
   SELECT coalesce(jsonb_agg(pg_temp.mask_json(v, field_name) ORDER BY ordinal), '[]'::jsonb)
   INTO result FROM jsonb_array_elements(value) WITH ORDINALITY AS item(v, ordinal);
   RETURN result;
 WHEN 'string' THEN
   scalar := value #>> '{}';
   IF lower(field_name) IN ('email', 'owneremail', 'assignee', 'contact_email') THEN
     RETURN to_jsonb(pg_temp.email_token(scalar));
   END IF;
   IF (field_name = 'submittedDate' AND scalar = '31/99/2026')
      OR (field_name = 'phase' AND scalar IN ('AWAITING_APPROVAL', 'COMPLETE'))
      OR (field_name = 'status' AND scalar IN ('WAITING', 'DONE'))
      OR (field_name = 'kind' AND scalar IN ('START', 'END'))
      OR (field_name = 'event' AND scalar = 'created') THEN
     RETURN value;
   END IF;
   RETURN to_jsonb('[MASKED]'::text);
 ELSE
   -- IDs, booleans and nulls are preserved in this synthetic fixture.
   RETURN value;
 END CASE;
END $$;

UPDATE masked.organisation SET name='Organisation ' || id,
 contact_email=pg_temp.email_token(contact_email);
UPDATE masked.application SET applicant_name='Applicant ' || id
 WHERE applicant_name IS NOT NULL;
UPDATE masked.participant SET email=pg_temp.email_token(email);
UPDATE masked.document SET filename='document-' || id || '.dat' WHERE filename IS NOT NULL;
UPDATE masked.attachment SET storage_key='masked/attachment-' || id WHERE storage_key IS NOT NULL;
UPDATE masked.comment SET body='[MASKED]' WHERE body IS NOT NULL;
UPDATE masked.external_reference SET reference_code='reference-' || id WHERE reference_code IS NOT NULL;

-- Apply the same JSON policy to every JSONB column, including history payloads.
DO $$
DECLARE col record;
BEGIN
 FOR col IN SELECT table_name, column_name FROM information_schema.columns
            WHERE table_schema='masked' AND data_type='jsonb'
 LOOP
   EXECUTE format('UPDATE masked.%I SET %I=pg_temp.mask_json(%I)',
                  col.table_name, col.column_name, col.column_name);
 END LOOP;
 IF pg_temp.mask_json('{"nested":{"email":"demo@example.invalid","note":"private"},"items":[{"ownerEmail":"demo@example.invalid"}]}'::jsonb)
    IS DISTINCT FROM jsonb_build_object(
      'nested', jsonb_build_object('email', pg_temp.email_token('demo@example.invalid'), 'note', '[MASKED]'),
      'items', jsonb_build_array(jsonb_build_object('ownerEmail', pg_temp.email_token('demo@example.invalid')))) THEN
   RAISE EXCEPTION 'Nested JSON masking consistency check failed';
 END IF;
END $$;
