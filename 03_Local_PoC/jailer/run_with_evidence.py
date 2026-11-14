"""Capture an actual Jailer CLI run and verify its export in a fresh disposable database."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
import uuid

root = Path(__file__).resolve().parents[1]
run_name = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:6]
folder = root / 'storage/jailer/work/evidence' / run_name
folder.mkdir(parents=True)
manifest = {'started_utc': datetime.now(timezone.utc).isoformat(), 'steps': [], 'success': False}

def run(args, filename, input_text=None):
    completed = subprocess.run(args, input=input_text, text=True, cwd=root,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (folder / filename).write_text(completed.stdout)
    manifest['steps'].append({'command': args, 'exit_code': completed.returncode, 'output': filename})
    if completed.returncode:
        raise RuntimeError(f'{filename}: command exited {completed.returncode}')
    return completed.stdout

def rows(database):
    tables = re.findall(r'CREATE TABLE (\w+)\(', (root / 'sql/01_schema.sql').read_text())
    clauses = [f'''SELECT '{t}' AS table_name, coalesce(jsonb_agg(to_jsonb(t) ORDER BY id), '[]'::jsonb) AS rows FROM public."{t}" t''' for t in tables]
    sql = 'SELECT jsonb_object_agg(table_name, rows) FROM (' + ' UNION ALL '.join(clauses) + ') snapshot'
    completed = subprocess.run(['docker','compose','exec','-T','db','psql','-X','-U','poc','-d',database,'-At','-v','ON_ERROR_STOP=1','-c',sql],
                               cwd=root, text=True, capture_output=True, check=True)
    return json.loads(completed.stdout)

created = False
test_db = 'poc_evidence_' + uuid.uuid4().hex[:12]
try:
    run(['docker','compose','up','-d','--wait','jailer'], 'container-start.log')
    cid = run(['docker','compose','ps','-q','jailer'], 'container-id.txt').strip()
    run(['docker','inspect',cid,'--format','{{json .}}'], 'container-inspect.json')
    run(['docker','compose','exec','-T','jailer','sh','/opt/jailer/jailer.sh','--version'], 'jailer-version.log')
    shutil.copytree(root / 'storage/jailer/work/models/defect-1001', folder / 'model')
    shutil.copy2(root / 'storage/jailer/work/defect-1001.jm', folder / 'extraction-model.jm')
    shutil.copy2(root / 'jailer/run_with_evidence.py', folder / 'evidence-runner.py')
    source_before = rows('poc')
    (folder / 'source-before.json').write_text(json.dumps(source_before, indent=2, sort_keys=True))
    args = ['docker','compose','exec','-T','jailer','sh','/opt/jailer/jailer.sh',
            'export', f'/work/evidence/{run_name}/extraction-model.jm',
            'org.postgresql.Driver','jdbc:postgresql://db:5432/poc','poc','poc_local_only',
            '-jdbcjar','lib/postgresql-42.7.4.jar','-datamodel',f'/work/evidence/{run_name}/model',
            '-scope','LOCAL_DATABASE','-local-database-storage','/work/tmp','-target-dbms','POSTGRESQL',
            '-format','SQL','-UTF8','-order-by-pk','-row-limit','1000',
            '-e',f'/work/evidence/{run_name}/jailer-subset.sql']
    run(args, 'jailer-export.log')
    run(['docker','compose','exec','-T','db','createdb','-U','poc',test_db], 'create-test-database.log')
    created = True
    run(['docker','compose','exec','-T','db','psql','-X','-U','poc','-d',test_db,'-v','ON_ERROR_STOP=1'],
        'restore-schema.log', (root / 'sql/01_schema.sql').read_text())
    run(['docker','compose','exec','-T','db','psql','-X','-U','poc','-d',test_db,'-v','ON_ERROR_STOP=1'],
        'restore-export.log', (folder / 'jailer-subset.sql').read_text())
    run(['docker','compose','exec','-T','db','psql','-X','-U','poc','-d',test_db,'-v','ON_ERROR_STOP=1'],
        'subset-assertions.log', (root / 'tests/check_subset.sql').read_text())
    restored = rows(test_db)
    (folder / 'restored-rows.json').write_text(json.dumps(restored, indent=2, sort_keys=True))
    if restored != rows('poc_subset'):
        raise RuntimeError('Fresh Jailer export restore differs from the verified unmasked subset')
    if source_before != rows('poc'):
        raise RuntimeError('Source records changed during evidence run')
    run([sys.executable,'tests/verify_defect_1001.py'], 'source-comparison.log')
    count = sum(len(value) for value in restored.values())
    manifest.update(success=True, exported_rows=count, exported_tables=len(restored), source_unchanged=True,
                    fresh_restore_matches_verified_subset=True)
    (folder / 'README.txt').write_text(
        f'Actual Jailer CLI run: {count} rows across {len(restored)} tables.\n'
        'jailer-export.log is captured process stdout/stderr, not a reconstructed summary.\n'
        'manifest.json records the exact commands and exit codes.\n'
        'jailer-subset.sql is the file written by Jailer.\n'
        'That export restored into a fresh disposable database with constraints enabled.\n'
        'Every restored value matches the verified unmasked subset. Source rows were unchanged.\n'
        'This run verifies extraction only. Masking is a separate SQL step in masking/policy.sql.\n'
        'SHA256SUMS records the captured artifacts for later integrity checks.\n')
finally:
    if created:
        try:
            run(['docker','compose','exec','-T','db','dropdb','-U','poc',test_db], 'cleanup-test-database.log')
        except Exception as error:
            manifest['cleanup_error'] = str(error)
            manifest['success'] = False
    manifest['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (folder / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    sums = []
    for path in sorted(folder.rglob('*')):
        if path.is_file() and path.name != 'SHA256SUMS':
            sums.append(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + str(path.relative_to(folder)))
    (folder / 'SHA256SUMS').write_text('\n'.join(sums) + '\n')
    (root / 'storage/jailer/work/evidence/LATEST.txt').write_text(run_name + '\n')
    print(folder)
    print(json.dumps({key: manifest.get(key) for key in ['success','exported_rows','exported_tables','source_unchanged','fresh_restore_matches_verified_subset']}))
if not manifest['success']:
    raise SystemExit(1)
