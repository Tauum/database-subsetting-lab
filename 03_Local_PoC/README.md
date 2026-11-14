# Mac local proof of concept

Requires Docker Desktop or Colima and Docker Compose. No IntelliJ, Java app, production data or original migrations needed.

## Start

From the project root, run `bash start.sh`. Or, from this folder:

```bash
mkdir -p storage/postgres storage/jailer/jailer storage/jailer/work/tmp
docker compose up -d --build --wait
bash tests/run_checks.sh
```

The Jailer Dockerfile automatically installs its pinned distribution into the local application folder. See [Docker setup](../DOCKER_SETUP.md).

Connect any SQL client to `localhost:55432`, database `poc`, username `poc`, password `poc_local_only`.

**Synthetic data only. Never expose this demonstration database to the public Internet.**

## Structure
- 12 domain tables + 12 matching history tables.
- Chain: organisation → process_instance → application → participant → document → attachment → attachment_metadata.
- Other branches: task, approval, comment, process_event, external_reference.
- `process_instance.state` is JSONB with malformed date and embedded reference.
- `external_reference.parent_process_id` is a logical reference with no FK and includes an orphan.
- Two processes share one organisation, illustrating possible over-extraction.
- Nullable `participant.referrer_id` demonstrates a cyclic/self-reference association.

## Storage

PostgreSQL data is stored in `storage/postgres/` inside this folder and excluded from Git. Keep exports and other generated lab files under `storage/` too. Docker images and container metadata remain in Docker Desktop’s managed storage.

## Reset

The bind-mounted database survives `docker compose down -v`. To reset the synthetic fixture, stop the container and move the data folder aside:
```bash
docker compose down
mv storage/postgres "storage/postgres-backup-$(date +%Y%m%d-%H%M%S)"
docker compose up -d
```

## Manual SQL examples
```bash
docker compose exec -T db psql -U poc -d poc < sql/03_inspect.sql
```

## Tool comparison
Point Jailer and Tonic at identical copies of this dataset. For Tonic Cloud, use a separate disposable network-accessible copy with only synthetic values. Never tunnel real production data.

## Export / restore smoke test
```bash
docker compose exec -T db pg_dump -U poc -d poc --data-only --inserts > local_data.sql
```
This is a **whole-demo export**, not a Jailer/Tonic subset. Restore a tool-generated subset against the matching schema and run the checks.

## What counts as a pass?
Correct target records and required dependencies; unrelated sibling process excluded; malformed JSON string unchanged; orphaned logical reference present when explicitly requested; history included; restore works; no masking leak.

## Jailer container

See [jailer/README.md](jailer/README.md) for the Docker CLI setup, schema discovery and local storage locations.
