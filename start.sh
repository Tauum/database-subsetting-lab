#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/03_Local_PoC"
mkdir -p storage/postgres storage/jailer/jailer storage/jailer/work/{models,exports,tmp}
docker compose up -d --build --wait
bash tests/run_checks.sh
bash jailer/run.sh --version
