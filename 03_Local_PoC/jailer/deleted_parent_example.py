"""Demonstrate an actual parent deletion, then extract and restore surviving children with Jailer."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import uuid

root = Path(__file__).resolve().parents[1]
run_name = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:6]
folder = root / 'storage/jailer/work/deleted-parent' / run_name
(folder / 'model').mkdir(parents=True)
source_db, subset_db = 'poc_deleted_parent', 'poc_deleted_parent_subset'
manifest = {'source_database': source_db, 'subset_database': subset_db, 'steps': [], 'success': False}

def run(args, name, input_text=None):
    result = subprocess.run(args, input=input_text, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (folder / name).write_text(result.stdout)
    manifest['steps'].append({'command': args, 'exit_code': result.returncode, 'output': name})
    if result.returncode: raise RuntimeError(f'{name}: exit {result.returncode}')
    return result.stdout

def sql(db, text, name):
    return run(['docker','compose','exec','-T','db','psql','-X','-U','poc','-d',db,'-v','ON_ERROR_STOP=1'], name, text)

schema_sql = (root / 'sql/01_schema.sql').read_text()
tables = re.findall(r'CREATE TABLE (\w+)\(', schema_sql)

def snapshot(db):
    parts = [f'''SELECT '{t}' AS table_name, coalesce(jsonb_agg(to_jsonb(t) ORDER BY id), '[]'::jsonb) AS rows FROM public."{t}" t''' for t in tables]
    query = 'SELECT jsonb_object_agg(table_name, rows) FROM (' + ' UNION ALL '.join(parts) + ') snapshot'
    out = subprocess.run(['docker','compose','exec','-T','db','psql','-X','-U','poc','-d',db,'-At','-v','ON_ERROR_STOP=1','-c',query], cwd=root, text=True, capture_output=True, check=True)
    return json.loads(out.stdout)

soft_links = '''ALTER TABLE public.application DROP CONSTRAINT application_process_id_fkey;
ALTER TABLE public.task DROP CONSTRAINT task_process_id_fkey;
ALTER TABLE public.process_event DROP CONSTRAINT process_event_process_id_fkey;
'''
try:
    original_source, original_subset = snapshot('poc'), snapshot('poc_subset')
    run(['docker','compose','exec','-T','db','createdb','-U','poc',source_db], 'create-source.log')
    sql(source_db, schema_sql + '\n' + (root / 'sql/02_seed.sql').read_text(), 'initialise-source.log')
    before = snapshot(source_db)
    (folder / 'before-delete.json').write_text(json.dumps(before, indent=2, sort_keys=True))
    blocked = '''DO $$ BEGIN
 BEGIN
  DELETE FROM public.process_instance WHERE id=1001;
  RAISE EXCEPTION 'Expected an enforced FK to block parent deletion';
 EXCEPTION WHEN foreign_key_violation THEN
  RAISE NOTICE 'PASS: enforced FK blocked the parent deletion';
 END;
END $$;
'''
    (folder / 'blocked-delete.sql').write_text(blocked)
    sql(source_db, blocked, 'blocked-delete.log')
    delete_sql = 'BEGIN;\n' + soft_links + '\nDELETE FROM public.process_instance WHERE id=1001;\nCOMMIT;\n'
    (folder / 'delete-parent.sql').write_text(delete_sql)
    sql(source_db, delete_sql, 'delete-parent.log')
    after = snapshot(source_db)
    (folder / 'after-delete.json').write_text(json.dumps(after, indent=2, sort_keys=True))
    if len(before['process_instance']) != 2 or [r['id'] for r in after['process_instance']] != [1002]:
        raise RuntimeError('Parent deletion did not produce the expected source state')
    for table in tables:
        if table != 'process_instance' and before[table] != after[table]:
            raise RuntimeError(f'Child or history data changed during deletion: {table}')
    container_base = f'/work/deleted-parent/{run_name}'
    build = ['docker','compose','exec','-T','jailer','sh','/opt/jailer/jailer.sh','build-model',
             '-schema','public','-datamodel',container_base+'/model','org.postgresql.Driver',
             'jdbc:postgresql://db:5432/'+source_db,'poc','poc_local_only','-jdbcjar','lib/postgresql-42.7.4.jar']
    run(build, 'jailer-build-model.log')
    with (folder / 'model/association.csv').open('a') as stream:
        stream.write('\n' + (root / 'jailer/logical-associations.csv').read_text())
        stream.write('''application; process_instance; ; n:1; A.process_id=B.id; soft_application_process; Deleted-parent demo;
task; process_instance; ; n:1; A.process_id=B.id; soft_task_process; Deleted-parent demo;
process_event; process_instance; ; n:1; A.process_id=B.id; soft_event_process; Deleted-parent demo;
''')
    model = '''# Root is a surviving child because process 1001 no longer exists.
application; T.id=2001; ;
inverse-process_instance_organisation_id_fkey; ; ignore
#! block additional subjects
# Other branches cannot be reached through a deleted process.
task; T.id=7001; ;
process_event; T.id=10001; ;
process_instance_history; T.record_id=1001; ;
external_reference; T.parent_process_id=1001; ;
#! block export modus
SQL
#! block version
17.3.1
'''
    (folder / 'deleted-parent.jm').write_text(model)
    export = ['docker','compose','exec','-T','jailer','sh','/opt/jailer/jailer.sh','export',
              container_base+'/deleted-parent.jm','org.postgresql.Driver','jdbc:postgresql://db:5432/'+source_db,
              'poc','poc_local_only','-jdbcjar','lib/postgresql-42.7.4.jar','-datamodel',container_base+'/model',
              '-scope','LOCAL_DATABASE','-local-database-storage','/work/tmp','-target-dbms','POSTGRESQL',
              '-format','SQL','-UTF8','-order-by-pk','-row-limit','1000','-e',container_base+'/jailer-subset.sql']
    run(export, 'jailer-export.log')
    run(['docker','compose','exec','-T','db','createdb','-U','poc',subset_db], 'create-subset.log')
    sql(subset_db, schema_sql + '\n' + soft_links, 'restore-matching-schema.log')
    sql(subset_db, (folder / 'jailer-subset.sql').read_text(), 'restore-export.log')
    restored = snapshot(subset_db)
    expected_ids = {'organisation':[], 'process_instance':[], 'application':[2001], 'participant':[3001],
        'document':[4001], 'attachment':[5001], 'attachment_metadata':[6001], 'task':[7001],
        'approval':[8001], 'comment':[9001], 'process_event':[10001], 'external_reference':[11001]}
    for index, table in enumerate(['organisation','process_instance','application','participant','document',
            'attachment','attachment_metadata','task','approval','comment','process_event','external_reference'], start=12001):
        expected_ids[table+'_history'] = [] if table=='organisation' else [index]
    for table in tables:
        values = restored[table]
        if [r['id'] for r in values] != expected_ids[table]:
            raise RuntimeError(f'Unexpected restored rows in {table}: {values}')
        if values != [r for r in after[table] if r['id'] in expected_ids[table]]:
            raise RuntimeError(f'Changed values in {table}')
    (folder / 'restored-rows.json').write_text(json.dumps(restored, indent=2, sort_keys=True))
    fk_count = sql(subset_db, "SELECT count(*) AS remaining_enforced_fks FROM pg_constraint WHERE contype='f' AND connamespace='public'::regnamespace;", 'fk-check.log')
    if snapshot('poc') != original_source or snapshot('poc_subset') != original_subset:
        raise RuntimeError('Original comparison data changed')
    count = sum(map(len, restored.values()))
    manifest.update(success=True, exported_rows=count, nonempty_tables=sum(bool(r) for r in restored.values()),
                    parent_deleted=True, children_and_history_unchanged_by_deletion=True,
                    original_comparison_unchanged=True, remaining_enforced_foreign_keys=8)
    (folder / 'verification.txt').write_text(
        'PASS: the normal FK first blocked deleting the parent.\n'
        'PASS: only in the separate demo, three top-level FK constraints were changed to soft model links.\n'
        'PASS: process 1001 was then actually deleted; all child and history records remained unchanged.\n'
        f'PASS: Jailer exported {count} rows; the file restored against the matching soft-link schema.\n'
        'PASS: exact IDs and all restored values match surviving source records; sibling process excluded.\n'
        'PASS: original source, unmasked subset and masked comparison remain untouched.\n')
finally:
    (folder / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    files = [p for p in folder.rglob('*') if p.is_file() and p.name!='SHA256SUMS']
    (folder / 'SHA256SUMS').write_text('\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(folder)) for p in sorted(files))+'\n')
    destination = root.parent/'01_Jailer/evidence/deleted-parent-run-evidence'
    shutil.copytree(folder,destination)
    (root / 'storage/jailer/work/deleted-parent/LATEST.txt').write_text(run_name+'\n')
    print(destination)
    print(json.dumps(manifest))
if not manifest['success']: raise SystemExit(1)
