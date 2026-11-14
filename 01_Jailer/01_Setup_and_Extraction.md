# Jailer: setup and extraction

## Inputs
- PostgreSQL JDBC connection URL and read-only credentials.
- Existing schema and actual populated records.
- Root table and selection condition, e.g. `process_instance.id = 1001`.
- An extraction model, including which associations are followed or restricted.

No Java application code or migration source is required for declared-FK traversal.

## Local evaluation
1. Download Jailer from its official project and check the current release and Java requirements.
2. Connect to the local PoC PostgreSQL service (`localhost:55432`, database `poc`, user `poc`).
3. Let Jailer introspect tables and FK associations.
4. Define root `process_instance` and condition `id = 1001`.
5. Inspect the association graph and exclude reverse traversals that pull unrelated processes via shared organisations.
6. Export SQL INSERTs to a local file.
7. Restore into a fresh schema/database and run the assertions in `03_Local_PoC/tests`.
8. Add explicit associations for JSONB keys if supported by your model, or document the missing edges.

## What to look for
- Does `process_instance → application → participant → document → attachment` extract fully?
- Are matching history rows included, or must you define history associations?
- Does the unrelated process for the same organisation get pulled in?
- Does a broken logical reference to a nonexistent parent remain present?
- Are SQL statements ordered so a fresh restore works?

## Security
Jailer export is not inherently anonymous. Keep raw exports restricted, encrypt storage, delete intermediates under policy, and require a validated masking/release stage before developer access.

## Caveat
Jailer interfaces and CLI flags vary by release; this document deliberately avoids inventing version-specific commands. Use the installed version's GUI or CLI help.
