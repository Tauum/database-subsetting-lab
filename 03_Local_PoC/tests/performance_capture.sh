#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
docker compose exec -T db psql -U poc -d poc -P pager=off -c "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM application WHERE process_id=1001;" | tee "results/explain_${stamp}.txt"
docker stats --no-stream | tee "results/docker_stats_${stamp}.txt"
echo "Record tool extraction duration separately; this script is source baseline only."
