# Jailer in Docker

Jailer 17.3.1 runs inside a persistent CLI container alongside PostgreSQL. No host Java installation is needed. This setup does not expose the Swing desktop GUI.

From `03_Local_PoC`:

```bash
bash jailer/setup.sh
bash jailer/run.sh --help
bash jailer/run.sh build-model -schema public -datamodel /work/models/poc org.postgresql.Driver jdbc:postgresql://db:5432/poc poc poc_local_only -jdbcjar lib/postgresql-42.7.4.jar
```

The Dockerfile downloads the official release and validates its published SHA-256. It pins the tested Java 21 image by digest and uses the bundled PostgreSQL JDBC driver. Run `bash start.sh` from the project root to build and start both containers. See `DOCKER_SETUP.md` at the project root.

All Jailer application files and logs are in `storage/jailer/jailer/`. Models, exports, temporary working files and saved command output are in `storage/jailer/work/`, mounted as `/work` in the container. Docker images and container metadata use Docker Desktop storage. The container stays running between jobs and is visible in Docker Desktop. The wrapper starts the service if needed and executes each Jailer command inside it. The container restarts with Docker unless explicitly stopped. It provides a CLI environment, not an HTTP server or automatic folder watcher. Run jobs sequentially against a shared model.

Stop the service with `docker compose stop jailer`; start it with `docker compose up -d jailer`.

`db:5432` is the database address within Compose. Desktop SQL clients continue to use `localhost:55432`.

## First verified defect subset

The synthetic process 1001 extraction and restore passed twice: 25 rows across 24 tables, including all 12 history rows and both external references. Process 1002 and its descendants are excluded. Every restored row matches its source values; the malformed date, embedded JSON participant reference and explicit logical orphan survive. Both exports have identical SQL statements after generated comments are removed.

Run from `03_Local_PoC`:

```bash
bash jailer/extract.sh
# Replaces only the disposable poc_subset database:
bash tests/restore_and_check.sh storage/jailer/work/exports/defect-1001.sql
python3 tests/verify_defect_1001.py
```

The restored database is `poc_subset` on the same local PostgreSQL service. The source `poc` stays available. Its normal fixture checks still pass.

`logical-associations.csv` explicitly links each history table and logical external reference. `defect-1001.jm` blocks reverse traversal through the shared organisation and adds orphan 11002 as a separate subject. Working tables are local to Jailer, rather than created in the source database. The job aborts above 1,000 exported rows.

This validates this fabricated fixture only. JSONB links are not auto-discovered: here participant 3001 is independently reached through declared FKs and its embedded ID is checked. The nullable self-reference contains no populated cycle, so a populated cycle has not been validated. Masking and performance at scale have not been evaluated.

Models and logs are under `storage/jailer/work/`; the latest export is `exports/defect-1001.sql`, restore output is `restore-check.log`, and assertions are recorded in `verification.txt`.

Official source and release: https://github.com/Wisser/Jailer/releases/tag/v17.3.1

## Capture evidence from a real Jailer run

After building the extraction model with `bash jailer/extract.sh`, run:

```bash
python3 jailer/run_with_evidence.py
```

This invokes the actual Jailer CLI inside its Docker container, captures its stdout/stderr and exit status, and saves the SQL file Jailer writes. It records container details and the exact model used. It restores that file into a fresh temporary database, checks the subset and every restored value against the verified unmasked subset, checks that source rows did not change, and removes the temporary database. The three comparison panes and their databases are preserved.

Each run gets a separate directory under `storage/jailer/work/evidence/`, containing `jailer-export.log`, `jailer-subset.sql`, `manifest.json`, model snapshots, restore logs, row snapshots and `SHA256SUMS`. `LATEST.txt` identifies the latest capture. Commands and logs are local reproducible evidence; checksums detect later artifact changes but are not independent third-party attestation.

Jailer performs extraction in this lab. The masking is our explicit PostgreSQL SQL stage in `masking/policy.sql`; it has not been demonstrated using Jailer's built-in masking features.
