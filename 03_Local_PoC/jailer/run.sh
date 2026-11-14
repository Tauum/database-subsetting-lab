#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose up -d --wait jailer >/dev/null
exec docker compose exec -T jailer sh /opt/jailer/jailer.sh "$@"
