-- Fabricated contact details for the JSON masking example. Idempotent.
BEGIN;
DO $$ BEGIN
 IF current_database() <> 'poc' THEN RAISE EXCEPTION 'Run against the synthetic source poc only'; END IF;
END $$;
UPDATE public.process_instance
SET state = state || jsonb_build_object('personalDetails', jsonb_build_object(
  'fullName', 'Alex Example',
  'email', 'demo@example.invalid',
  'phone', '+44 7700 900123',
  'address', jsonb_build_object('line1', '10 Example Street', 'city', 'Exampleton', 'postcode', 'EX4 1PL')
)) WHERE id=1001;
COMMIT;
