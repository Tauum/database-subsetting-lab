"""Validate the exact synthetic subset and compare every restored value to source."""
import json
import subprocess

expected = {
    "organisation": [1], "process_instance": [1001], "application": [2001],
    "participant": [3001], "document": [4001], "attachment": [5001],
    "attachment_metadata": [6001], "task": [7001], "approval": [8001],
    "comment": [9001], "process_event": [10001], "external_reference": [11001, 11002],
}
for index, table in enumerate(list(expected), start=12001):
    expected[table + "_history"] = [index]

def query(database, sql):
    result = subprocess.run(
        ["docker", "compose", "exec", "-T", "db", "psql", "-X", "-U", "poc",
         "-d", database, "-At", "-v", "ON_ERROR_STOP=1", "-c", sql],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)

rows = 0
for table, ids in expected.items():
    sql = f"""SELECT coalesce(json_agg(t ORDER BY id), '[]'::json) FROM "{table}" t"""
    actual = query("poc_subset", sql)
    actual_ids = [row["id"] for row in actual]
    if actual_ids != ids:
        raise SystemExit(f"Unexpected rows in {table}: {actual_ids}; expected {ids}")
    source_sql = sql + " WHERE id IN (" + ",".join(map(str, ids)) + ")"
    if actual != query("poc", source_sql):
        raise SystemExit(f"Restored values differ from source in {table}")
    rows += len(actual)

process = query("poc_subset", "SELECT row_to_json(t) FROM process_instance t WHERE id=1001")
if process["state"].get("submittedDate") != "31/99/2026":
    raise SystemExit("Malformed date was changed")
if process["state"].get("embeddedParticipantId") != 3001:
    raise SystemExit("Embedded JSON participant reference was changed")
orphan = query("poc_subset", "SELECT row_to_json(t) FROM external_reference t WHERE id=11002")
if orphan["parent_process_id"] != 999999:
    raise SystemExit("Logical orphan was changed")
print(f"PASS: {rows} rows across {len(expected)} tables; exact IDs and all values match source.")
print("PASS: sibling excluded; all 12 histories, full attachment chain, malformed date, JSON reference and logical orphan preserved.")
