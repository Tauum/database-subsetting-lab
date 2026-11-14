#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
work=storage/jailer/work
bash jailer/run.sh build-model -schema public -datamodel /work/models/poc org.postgresql.Driver jdbc:postgresql://db:5432/poc poc poc_local_only -jdbcjar lib/postgresql-42.7.4.jar > "$work/build-model.log" 2>&1
mkdir -p "$work/models/defect-1001" "$work/exports"
cp "$work/models/poc/"*.csv "$work/models/defect-1001/"
cat jailer/logical-associations.csv >> "$work/models/defect-1001/association.csv"
cp jailer/defect-1001.jm "$work/defect-1001.jm"
bash jailer/run.sh export /work/defect-1001.jm org.postgresql.Driver jdbc:postgresql://db:5432/poc poc poc_local_only -jdbcjar lib/postgresql-42.7.4.jar -datamodel /work/models/defect-1001 -scope LOCAL_DATABASE -local-database-storage /work/tmp -target-dbms POSTGRESQL -format SQL -UTF8 -order-by-pk -row-limit 1000 -e /work/exports/defect-1001.sql > "$work/extraction.log" 2>&1
echo "Exported $work/exports/defect-1001.sql"
