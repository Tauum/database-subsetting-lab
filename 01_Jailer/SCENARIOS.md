# Reproduce the Jailer scenarios

All data is fabricated. Jailer performs extraction; the SQL masking policy is a separate stage. Requires Docker with Compose, Bash and Python 3 for the runners and verification.

From the project root, start the lab:

```bash
bash start.sh
cd 03_Local_PoC
```

## Scenario 1: extract a defect subset and mask JSON

On a fresh lab:

```bash
# Add fabricated personal details inside the target process JSON.
docker compose exec -T db psql -X -U poc -d poc -v ON_ERROR_STOP=1 < sql/09_add_personal_json_example.sql
bash jailer/extract.sh
# Replaces the disposable poc_subset database:
bash tests/restore_and_check.sh storage/jailer/work/exports/defect-1001.sql
python3 masking/create_masked.py
python3 tests/verify_defect_1001.py
python3 tests/verify_masked_subset.py
```

Expected result: 35 source rows become 25 subset rows across 24 tables. Process 1002 is excluded. All matching history is included. Personal JSON names, phone numbers and addresses are masked; repeated emails receive consistent replacements. The malformed date `31/99/2026` and relationship IDs survive.

SQL client: `localhost:55432`, user `poc`, password `poc_local_only`. Compare `poc.public`, `poc_subset.public` and `poc_subset.masked`. Open `sql/08_compare_masked.sql` using the subset connection.

To capture the actual Jailer command, raw output, SQL file and a fresh-restore verification:

```bash
python3 jailer/run_with_evidence.py
python3 jailer/write_table_report.py
```

Reports and raw evidence are generated locally. They are excluded from Git; the repository contains the inputs, runners and checks needed to reproduce them.

## Scenario 2: delete a parent and extract surviving children

```bash
python3 jailer/deleted_parent_example.py
```

The runner creates two separate databases and refuses to overwrite existing ones. It first proves that an enforced FK blocks deletion. In the isolated fixture only, it changes three direct process links to soft references, then actually deletes process 1001 while its children and history remain.

Jailer starts from a surviving child and explicitly selected disconnected branches. It exports 21 rows and restores them against the matching soft-link schema. Eight other foreign keys stay enforced. The original scenario 1 databases remain unchanged.

Inspect `poc_deleted_parent` and `poc_deleted_parent_subset`. Raw run artifacts are saved locally under `03_Local_PoC/storage/jailer/work/deleted-parent/`, with a readable evidence copy generated beneath `01_Jailer/evidence/`.

## Re-running and local files

- The scenario 1 restore command replaces only its disposable subset database, including an existing masked schema.
- The masked-schema creator refuses to overwrite that schema.
- The deleted-parent runner refuses to overwrite its named databases.
- The local evidence folders, image exports, Docker bind data, downloaded Jailer distribution and IDE settings are not repository inputs.
- See [Docker setup](../DOCKER_SETUP.md) and [masking policy notes](../03_Local_PoC/masking/README.md).
