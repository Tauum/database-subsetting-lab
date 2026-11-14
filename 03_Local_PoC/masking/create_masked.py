"""Create the masked schema in the local synthetic subset, transactionally."""
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[1]
schema = (root / 'sql/01_schema.sql').read_text()
tables = re.findall(r'CREATE TABLE (\w+)\(', schema)
assert len(tables) == 24
statements = [
    'BEGIN;',
    "DO $$ BEGIN IF current_database() <> 'poc_subset' THEN RAISE EXCEPTION 'Wrong database'; END IF; END $$;",
    'CREATE SCHEMA masked;',
    "COMMENT ON SCHEMA masked IS 'Synthetic subsetting lab: masking policy v1';",
    'SET LOCAL search_path TO masked, pg_catalog;',
    schema,
]
for table in tables:
    statements.append(f'INSERT INTO masked."{table}" SELECT * FROM public."{table}" ORDER BY id;')
statements += [(root / 'masking/policy.sql').read_text(), 'COMMIT;']
subprocess.run(
    ['docker', 'compose', 'exec', '-T', 'db', 'psql', '-X', '-U', 'poc', '-d', 'poc_subset',
     '-v', 'ON_ERROR_STOP=1'],
    input='\n'.join(statements), text=True, check=True, cwd=root,
)
print('Created poc_subset.masked; public remains unmasked. Existing masked schemas are never overwritten.')
