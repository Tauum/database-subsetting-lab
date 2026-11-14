# Side-by-side scorecard

| Test | Jailer result | Tonic result | Evidence |
|---|---|---|---|
| Root 1001 selected | | | |
| All expected FK descendants | | | |
| Unrelated process 1002 excluded | | | |
| History rows included | | | |
| JSON `embeddedParticipantId` handled | | | |
| Malformed date `31/99/2026` retained | | | |
| Orphan `parent_process_id=999999` included when explicitly selected | | | |
| Masked email and JSON ownerEmail | | | |
| Restore to clean schema works | | | |
| Time to configure (minutes) | | | |
| Extraction elapsed time (seconds) | | | |
| Rows / size exported | | | |
| Source query load / replica lag | | | |
| Manual repair effort (minutes) | | | |

**Pass:** defect reproduced locally, no sensitive values leaked, and operator effort is acceptable.
