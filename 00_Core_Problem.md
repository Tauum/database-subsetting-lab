# Core issue and requirements

## Context
- Java backend, PostgreSQL, BPMN-based process engine.
- Four environments; some synthetic, one production-like but stale and controlled for customer/BA testing, and production.
- Approximately 400 tables, roughly half history tables; JSON/JSONB persists workflow state and view data.
- Developers need to reproduce real defects (malformed JSON date, missing parent, inconsistent history) and test fixes locally.
- No existing end-to-end fixtures, no practical time to hand-author 400-table data, and no appetite for extra permanent infrastructure.
- Production-derived data cannot simply be copied to developers, including international teams, without approval and suitable controls.
- Existing schema migrations exist; the requirement is data extraction, not schema discovery from Java code.

## Desired workflow
1. Developer records a defect and root table/key.
2. Approved operator initiates a bounded subset extraction from a production read replica (if one exists).
3. Extract related records, including history and configured non-FK relationships.
4. Preserve the *defect signature*, mask sensitive values, and verify privacy and technical completeness.
5. Package an approved SQL fixture or restorable backup.
6. Developer restores locally, reproduces the original error, tests fix, and stores the fixture as regression evidence.

## Non-goals
- Synthesising every possible process state from scratch.
- Executing workflows via UI/API to build fixtures.
- Mirroring all production data to developer machines.
- Sending raw personal data to external AI services.

## Success criteria
- One identifier yields a usable defect-centred subset with no manual reconstruction.
- Exact failing condition survives transformation.
- Extracted rows and traversal paths are explainable and bounded.
- Fixture is reproducible, versioned, approved, and imports on a clean schema.
- Review effort and elapsed turnaround are measured, not assumed.

## Fundamental limitations
FK traversal cannot discover all implicit JSONB, Java, or BPMN relationships. Orphaned logical records may not be reachable from their missing parent. Referentially valid subsets are not necessarily application-valid. Anonymisation is not established merely by replacing names.
