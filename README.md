# PostgreSQL defect-reproduction and subsetting evaluation

**Purpose:** Evaluate extracting a defect-centred, relationally consistent subset of PostgreSQL data, protecting personal information, and giving developers a locally restorable fixture. The proof of concept uses **only fabricated data**.

## Contents
- `00_Core_Problem.md`: problem, constraints, desired outcome, decision boundaries.
- `00_Tool_Comparison.md`: Jailer versus Tonic Structural, trade-offs and decision matrix.
- `01_Jailer/`: deployment, workflow, risks and evaluation.
- `02_Tonic_Structural/`: trial, deployment, output and evaluation.
- `03_Local_PoC/`: runnable Mac-friendly PostgreSQL demo, scenarios, tests and performance plan.
- `04_Governance/`: production-safe operational model, privacy review, handoff and risk register.

## Start on a Mac

With Docker running, execute from this project folder:

```bash
bash start.sh
```

This builds Jailer, starts both containers and checks the source fixture. See [DOCKER_SETUP.md](DOCKER_SETUP.md) for pinned versions, local storage and scenario rerun instructions.

The demo is intentionally **not a reproduction of your real application**. It has 12 domain tables and 12 matching history tables, with JSONB, multiple FK depths, shared parents, cycles via nullable references, and a deliberately broken logical reference.

## Important boundaries
- A relational subset can be complete under declared FKs yet incomplete for JSONB and application-level references.
- A deliberately orphaned logical reference is modelled without an enforced FK; an enforced FK would normally prevent it.
- Masking must preserve the defect being tested and must be reviewed before any production-derived data leaves a restricted area.
- Pricing, licensing, trial availability, APIs and product features change. Validate them against current vendor documentation before committing.

## Reproduce the scenarios

See [SCENARIOS.md](01_Jailer/SCENARIOS.md) for extraction, JSON masking, the deleted-parent case and optional local evidence generation. Captured results and database storage are excluded from Git.
