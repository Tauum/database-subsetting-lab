# Mac setup and smoke test
Install Docker Desktop or Colima with Docker CLI and Compose plugin. From `03_Local_PoC`:
```bash
docker compose up -d
docker compose exec -T db pg_isready -U poc -d poc
bash tests/run_checks.sh
```
The schema is automatically initialised on the first startup. Inspect tables with `docker compose exec -T db psql -U poc -d poc -c '\dt'`.
Connect a PostgreSQL client to 127.0.0.1:55432, database/user `poc`, password `poc_local_only`. Only synthetic data. To reset: `docker compose down -v && docker compose up -d`. PostgreSQL image is pinned to major version 16; pin digest for strict reproducibility.
