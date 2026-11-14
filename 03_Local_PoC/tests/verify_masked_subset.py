"""Validate this fabricated fixture's masked schema, without treating it as anonymised."""
from pathlib import Path
import json
import re
import subprocess

root = Path(__file__).resolve().parents[1]
tables = re.findall(r'CREATE TABLE (\w+)\(', (root / 'sql/01_schema.sql').read_text())

def query(sql):
    out = subprocess.run(['docker', 'compose', 'exec', '-T', 'db', 'psql', '-X', '-U', 'poc',
                          '-d', 'poc_subset', '-At', '-v', 'ON_ERROR_STOP=1', '-c', sql],
                         cwd=root, check=True, text=True, capture_output=True)
    return json.loads(out.stdout)

def require(condition, message):
    if not condition:
        raise SystemExit(message)

original, masked = {}, {}
for table in tables:
    for schema, snapshot in [('public', original), ('masked', masked)]:
        snapshot[table] = query(f'''SELECT coalesce(json_agg(t ORDER BY id), '[]'::json) FROM {schema}."{table}" t''')
    require([r['id'] for r in original[table]] == [r['id'] for r in masked[table]], f'Row membership changed: {table}')

sensitive_columns = {
    'organisation': {'name', 'contact_email'}, 'application': {'applicant_name'},
    'participant': {'email'}, 'document': {'filename'}, 'attachment': {'storage_key'},
    'comment': {'body'}, 'external_reference': {'reference_code'},
}
allowed_operational_strings = {'31/99/2026', 'AWAITING_APPROVAL', 'WAITING', 'START', 'created'}
original_sensitive = set()

def json_strings(value):
    if isinstance(value, dict):
        for item in value.values(): yield from json_strings(item)
    elif isinstance(value, list):
        for item in value: yield from json_strings(item)
    elif isinstance(value, str): yield value

def check_shape(before, after):
    if isinstance(before, dict):
        require(isinstance(after, dict) and before.keys() == after.keys(), 'JSON keys changed')
        for key in before: check_shape(before[key], after[key])
    elif isinstance(before, list):
        require(isinstance(after, list) and len(before) == len(after), 'JSON array shape changed')
        for left, right in zip(before, after): check_shape(left, right)
    elif not isinstance(before, str):
        require(before == after, 'JSON ID, number, boolean or null changed')
    else:
        require(isinstance(after, str), 'JSON string type changed')

for table in tables:
    for before, after in zip(original[table], masked[table]):
        require(before.keys() == after.keys(), f'Columns changed: {table}')
        for column, value in before.items():
            new_value = after[column]
            if column in sensitive_columns.get(table, set()):
                if value is not None:
                    original_sensitive.add(value)
                    require(value != new_value and new_value is not None, f'Not masked: {table}.{column}')
            elif isinstance(value, (dict, list)):
                check_shape(value, new_value)
                original_sensitive.update(set(json_strings(value)) - allowed_operational_strings)
            else:
                require(value == new_value, f'Unapproved change: {table}.{column}')

serialized = json.dumps(masked).lower()
for value in original_sensitive:
    require(value.lower() not in serialized, f'Original sensitive value survived masking: {value}')

before_state = original['process_instance'][0]['state']
after_state = masked['process_instance'][0]['state']
for field in ('submittedDate', 'embeddedParticipantId', 'phase'):
    require(before_state[field] == after_state[field], f'Defect field changed: {field}')
if 'personalDetails' in before_state:
    details = after_state['personalDetails']
    require(details['fullName'] == '[MASKED]' and details['phone'] == '[MASKED]', 'Personal JSON name or phone not masked')
    require(all(value == '[MASKED]' for value in details['address'].values()), 'Nested address not masked')
    require(details['email'] == masked['participant'][0]['email'], 'Personal JSON email token differs from participant email')
    print('PASS: personal JSON name, phone and nested address masked; email token matches the participant column.')
require(original['process_event'] == masked['process_event'], 'Operational event changed')
for table in tables:
    if table.endswith('_history'):
        require(original[table] == masked[table], f'Non-sensitive fixture history changed: {table}')
email = masked['participant'][0]['email']
require(re.fullmatch(r'masked-[0-9a-f]{32}@example\.invalid', email) is not None, 'Email token has unexpected format')
require(email == masked['task'][0]['state']['assignee'] == masked['attachment_metadata'][0]['metadata']['ownerEmail'], 'Email replacements are inconsistent across column and JSON')
require(email != masked['organisation'][0]['contact_email'], 'Different email identities were merged')

constraints = query('''SELECT json_agg(json_build_object('type', c.contype, 'valid', c.convalidated,
 'target_schema', target_ns.nspname)) FROM pg_constraint c
 JOIN pg_namespace ns ON ns.oid=c.connamespace
 LEFT JOIN pg_class target ON target.oid=c.confrelid
 LEFT JOIN pg_namespace target_ns ON target_ns.oid=target.relnamespace
 WHERE ns.nspname='masked' ''')
fks = [c for c in constraints if c['type'] == 'f']
require(len(fks) == 11 and all(c['valid'] and c['target_schema'] == 'masked' for c in fks), 'Masked foreign keys missing, unvalidated or pointing at public')
require(sum(c['type'] == 'p' for c in constraints) == 24, 'Masked primary keys missing')
require(sum(map(len, masked.values())) == 25, 'Unexpected masked row count')
print('PASS: 25 rows across 24 masked tables; original sensitive fixture strings absent.')
print('PASS: consistent email tokens across columns and JSON; IDs, defect payload and history preserved.')
print('PASS: all 24 primary keys and 11 validated foreign keys retained; FKs target masked tables.')
