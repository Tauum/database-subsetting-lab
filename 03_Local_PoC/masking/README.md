# Synthetic subset masking, policy v1

The `poc_subset` database now contains an unmasked `public` schema and a masked `masked` schema. The source database `poc` is separate. Both subset schemas have 25 rows across 24 tables, including all history rows. The masked tables have their own 24 primary keys and 11 validated foreign keys, all referencing masked tables.

This is an explicit SQL masking stage after Jailer extraction, not a test of Jailer's built-in masking or Tonic. It demonstrates the workflow on fabricated data only.

## Policy

| Data | Action |
|---|---|
| Organisation and applicant names | Replace with ID-based synthetic labels |
| Email columns and email values in JSON | Same deterministic replacement for the same normalised original |
| Comment bodies, filenames, storage keys, external reference codes | Replace with generic values or ID-based labels |
| JSON strings | Retain only the fixture's explicitly allowed operational values; mask other strings, recursively through objects and arrays |
| IDs, FK values, JSON numbers, booleans, nulls | Preserve |
| Malformed submitted date and defect state | Preserve exactly |
| History | Copy all rows; apply the JSON policy to every JSONB payload |

Email tokens use unsalted MD5 solely for repeatable synthetic-demo replacements. They are linkable and guessable, and do not establish anonymisation. This is not a production masking policy. JSON keys are retained; numeric sensitive fields are not masked. The sample history payloads contain record IDs and creation events, so their values stay unchanged; nested JSON handling is separately asserted during creation.

## Run and inspect

From `03_Local_PoC`, after extraction and restore:

```bash
python3 masking/create_masked.py
python3 tests/verify_masked_subset.py
python3 tests/verify_defect_1001.py
```

Creation uses a single transaction and refuses to overwrite an existing `masked` schema. Re-running the existing restore procedure recreates the disposable `poc_subset` database and removes its masked schema too; recreate masking afterwards.

Open `sql/08_compare_masked.sql` using the restored-subset connection in IntelliJ. Refresh that connection and select the `masked` schema if it is not already visible. Compare the two application names or participant emails; the malformed date, phase and embedded participant reference should remain identical. Personal details inside the state JSON should change.

Validation checks exact row IDs, all original sensitive fixture strings across the masked data, email consistency across tables and JSON, the unchanged defect, preserved nonsensitive fields, and all primary/foreign keys. The original public subset still passes its exact source-value comparison.

Creation output: `storage/jailer/work/masking-create.log`. Results: `storage/jailer/work/masking-verification.txt`. Masked-only export: `storage/jailer/work/exports/defect-1001-masked.sql`.

PostgreSQL references: [schema search path](https://www.postgresql.org/docs/16/ddl-schemas.html#DDL-SCHEMAS-PATH), [JSONB functions](https://www.postgresql.org/docs/16/functions-json.html).

## Personal information inside the process JSON

A second example adds fabricated personal details to process 1001: name, email, phone and a nested address. The recursive JSON policy masks the name, phone and address strings, and gives the email the same token as the participant column. The malformed submittedDate, phase and embeddedParticipantId remain unchanged.

To repeat this example while preserving existing table objects and IntelliJ panes:

```bash
docker compose exec -T db psql -X -U poc -d poc -v ON_ERROR_STOP=1 < sql/09_add_personal_json_example.sql
bash jailer/extract.sh
python3 masking/refresh_from_export.py
python3 tests/verify_masked_subset.py
python3 tests/verify_defect_1001.py
```

The refresh script replaces only the two disposable subset schemas' rows, in one transaction. It checks the database, the lab schema marker and the expected table layout first. It retains the schema and table objects, constraints and IDs. Refresh the open table results in IntelliJ afterwards.

The supplemental JSON fixture is not loaded automatically by the initial seed. Run the command above after a reset to recreate it. This remains a SQL masking stage after Jailer extraction, not a test of Jailer's built-in filters.

Second-example validation output: `storage/jailer/work/json-example-verification.txt`.
