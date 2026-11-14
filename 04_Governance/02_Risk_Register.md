# Risk register

| Risk | Impact | Mitigation / proof |
|---|---|---|
| Missing JSON/BPMN links | Incomplete fixture | Map implicit edges, validate defect-specific closure |
| Over-extraction via shared parent | High source load / privacy exposure | Directional association restrictions, row budgets |
| Inconsistent snapshot | Mixed-time records | Validate snapshot consistency and replica behaviour |
| Missing orphan | False negative | Explicitly seed/extract orphan child as additional root |
| Masking removes bug | Failure cannot reproduce | Preserve and assert exact malformed payload |
| Sensitive data leakage | Compliance/security incident | Restricted staging, automated masking, privacy review |
| SQL expert bottleneck | Slow delivery | Batch review, reusable mappings, track handling time |
| Schema drift | Broken exports | Versioned extraction model, schema compatibility checks |
| Restore dependency gap | Import succeeds but app fails | Restore test, app startup, reproduction assertion |
| Licence/vendor constraints | Blocked deployment | Trial evaluation and procurement verification |
| Replica load / lag | Production operational risk | Schedule, monitor, cap job concurrency |
| Developer copies persist | Uncontrolled retention | Expiry, access controls, inventory and deletion |
