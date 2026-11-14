# Jailer vs Tonic Structural

| Criterion | Jailer | Tonic Structural |
|---|---|---|
| Primary function | Relational subsetting and SQL export | Relational subsetting with configurable masking |
| PostgreSQL | Supported | Supported |
| Starting from a root record | Supported through extraction model/condition | Supported through configured subsetting rules |
| FK traversal | Yes | Yes |
| Implicit JSON relationships | Custom association/rule work | Custom rules/configuration; verify exact support |
| SQL INSERT output | Native capability | Do **not** assume direct Flyway SQL output |
| Typical output path | File export | Usually a destination database |
| Built-in comprehensive de-identification | Not a turnkey guarantee | Key product capability; still needs policy validation |
| On-premises | Local Java tool | Commercial self-hosted option; confirm entitlement |
| Cost | Open-source | Commercial; confirm trial, tier and licensing |
| Main risk | Masking effort, implicit relationships | Cost, destination dependency, masking correctness |

## Decision gate
Test identical fabricated source datasets and root identifiers. Compare completeness, time to configure, rows exported, output format, preserved malformed JSON, missing logical parent, masking coverage, restore success and measured source load.

## Recommended initial route
Run Jailer locally first for direct SQL export; evaluate Tonic using a trial on synthetic data if accessible. Do not purchase either workflow's operational assumptions without a successful defect-fidelity test.

## Claims to verify before procurement
Current product version, license terms, cloud-trial length, on-prem entitlement, telemetry, supported JSON transformations, API automation, source/destination constraints and export formats. Treat earlier conversational price/trial claims as unverified until checked with the vendor.
