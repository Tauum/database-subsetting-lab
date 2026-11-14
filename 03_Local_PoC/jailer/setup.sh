#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p storage/postgres storage/jailer/jailer storage/jailer/work/{models,exports,tmp}
docker compose up -d --build --wait jailer
exec bash jailer/run.sh --version
