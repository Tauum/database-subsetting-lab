# Tonic Structural: deployment and workflow

## Inputs
- Source PostgreSQL database credentials and network access.
- Workspace/subsetting configuration rooted at selected records.
- Masking policies for columns and JSON paths.
- A destination for generated data in the commonly documented database-to-database workflow.

No Java backend or original migration scripts required for ordinary schema-based subsetting.

## Local trial using fake data
1. Confirm current free-trial eligibility and whether a cloud or self-hosted evaluation is available.
2. Run `03_Local_PoC` PostgreSQL on the Mac.
3. If using Tonic Cloud, provide an approved network-accessible disposable test database; `localhost` alone will not be reachable.
4. Configure PostgreSQL source, select a root ID, inspect discovered FK graph.
5. Configure deterministic masking of names/emails and JSON paths, while explicitly preserving malformed date format.
6. Generate into an isolated destination database **if required by the chosen product workflow**.
7. Export destination using `pg_dump` or equivalent, restore locally and run assertions.
8. Capture masking coverage and defect fidelity.

## Output caveat
Do not assume native direct SQL migration or `.dump` output. Confirm with vendor documentation or support. If a destination is required, it can be a disposable database rather than a permanent server.

## On-premise caveat
Confirm licensing, telemetry, model of deployment, retention, API entitlements and whether data ever leaves your network. Self-hosted does not itself establish GDPR compliance.
