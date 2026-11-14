#!/usr/bin/env bash
set -euo pipefail
# Usage: ./tests/restore_and_check.sh path/to/subset.sql
# Only run against the local disposable Docker instance.
cd "$(dirname "$0")/.."
test "$#" -eq 1 || { echo "Usage: $0 subset.sql"; exit 2; }
fixture="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
test -f "$fixture"
docker compose exec -T db psql -U poc -d postgres -v ON_ERROR_STOP=1 -c 'DROP DATABASE IF EXISTS poc_subset WITH (FORCE);'
docker compose exec -T db psql -U poc -d postgres -v ON_ERROR_STOP=1 -c 'CREATE DATABASE poc_subset;'
docker compose exec -T db psql -U poc -d poc_subset -v ON_ERROR_STOP=1 < sql/01_schema.sql
docker compose exec -T db psql -U poc -d poc_subset -v ON_ERROR_STOP=1 < "$fixture"
docker compose exec -T db psql -U poc -d poc_subset -v ON_ERROR_STOP=1 < tests/check_subset.sql
