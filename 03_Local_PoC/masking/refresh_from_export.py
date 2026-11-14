"""Refresh the two disposable subset schemas in place, preserving IntelliJ table objects."""
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[1]
tables = re.findall(r'CREATE TABLE (\w+)\(', (root / 'sql/01_schema.sql').read_text())
assert len(tables) == 24
statements = ['BEGIN;', '''DO $$ BEGIN
 IF current_database() <> 'poc_subset' OR
    obj_description('masked'::regnamespace) IS DISTINCT FROM 'Synthetic subsetting lab: masking policy v1'
 THEN RAISE EXCEPTION 'Expected the disposable subset database and lab-generated masked schema'; END IF;
 IF (SELECT count(*) FROM information_schema.tables WHERE table_schema IN ('public','masked') AND table_type='BASE TABLE') <> 48
 THEN RAISE EXCEPTION 'Unexpected subset schema layout'; END IF;
 END $$;''', 'SET LOCAL search_path TO public, pg_catalog;']
statements.append('TRUNCATE ' + ', '.join(f'{schema}."{table}"' for schema in ['public', 'masked'] for table in tables) + ';')
statements.append((root / 'storage/jailer/work/exports/defect-1001.sql').read_text())
for table in tables:
    statements.append(f'INSERT INTO masked."{table}" SELECT * FROM public."{table}" ORDER BY id;')
statements += [(root / 'masking/policy.sql').read_text(), 'COMMIT;']
subprocess.run(['docker', 'compose', 'exec', '-T', 'db', 'psql', '-X', '-U', 'poc', '-d', 'poc_subset',
                '-v', 'ON_ERROR_STOP=1'], input='\n'.join(statements), text=True, check=True, cwd=root)
print('Refreshed unmasked and masked subsets from the latest Jailer export, in one transaction.')
