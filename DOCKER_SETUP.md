# Reproduce the Docker lab

From the project folder, run:

```bash
bash start.sh
```

Requires Docker with Compose and a running Docker daemon. The initial build downloads the pinned Jailer release and verifies its SHA-256. No host Java, curl or unzip installation is needed.

The startup script builds Jailer, starts PostgreSQL and the persistent Jailer container, waits for health checks, and runs the source-fixture checks. On fresh storage PostgreSQL creates the 24 tables and fabricated seed records. Existing database files are reused.

## Files

- `03_Local_PoC/docker-compose.yml` defines both services, local mounts, health checks and networking.
- `03_Local_PoC/jailer/Dockerfile` packages Jailer 17.3.1 with the tested Java 21 runtime.
- `03_Local_PoC/jailer/bootstrap.sh` populates the application mount from the image on a fresh checkout.
- `start.sh` is the project-level startup command.

PostgreSQL and Java base images are pinned by digest. Jailer is pinned by release and archive checksum. The image-build tooling needs network access; the finished application files are pinned inputs.

## Storage and connection

All database data, Jailer application files, models, logs and exports stay beneath `03_Local_PoC/storage/` in this project. Docker images, build cache and container metadata use Docker Desktop's storage.

SQL client connection: `localhost:55432`, database `poc`, user `poc`, password `poc_local_only`. The password is only for this fabricated local lab. PostgreSQL listens on the host's loopback interface.

## Stop or restart

From `03_Local_PoC`:

```bash
docker compose stop
docker compose up -d --wait
```

Stopping or recreating containers retains the bind-mounted data. Even `docker compose down -v` does not reset these host folders.

## Recreate the examples on a fresh lab

Container startup seeds the source fixture. It does not automatically run extraction, masking or deletion scenarios. With Python 3 installed, run these commands from `03_Local_PoC` for the first example:

```bash
bash jailer/extract.sh
bash tests/restore_and_check.sh storage/jailer/work/exports/defect-1001.sql
python3 masking/create_masked.py
python3 tests/verify_masked_subset.py
```

The restore command replaces the disposable `poc_subset` database. The masking creator refuses to overwrite an existing masked schema. For the JSON personal-data addition and deleted-parent case, see their separate evidence pages:

- [Subset and masking scenario](01_Jailer/SCENARIOS.md#scenario-1-extract-a-defect-subset-and-mask-json)
- [Deleted-parent scenario](01_Jailer/SCENARIOS.md#scenario-2-delete-a-parent-and-extract-surviving-children)
- [JSON example rerun instructions](03_Local_PoC/masking/README.md)

## Clean-storage verification

The Docker build and startup were tested using a separate Compose project, empty storage, a separate network and no published port. Both services became healthy; the source fixture checks and Jailer schema discovery were checked there. Test output is retained under `03_Local_PoC/storage/repro-check/`. The temporary test containers are stopped after verification.

Docker references: [checksum-verified build inputs](https://docs.docker.com/build/policies/), [service health and startup order](https://docs.docker.com/compose/how-tos/startup-order/).
