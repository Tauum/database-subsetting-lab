# Performance test plan

1. Establish baseline query latency and PostgreSQL CPU/I/O on the synthetic source.
2. Record Jailer/Tonic versions, configurations, selected root and connection pool size.
3. Run 1, 5 and 20 sequential extraction requests; separately test concurrency 2 only if safe.
4. Scale fabricated data by inserting additional processes and descendants (never production data). Preserve a known root for completeness checks.
5. Record wall time, exported rows/bytes, source SQL duration, memory, destination bytes and failure count.
6. On a real replica, require operational approval and monitor replay lag, query conflicts, WAL retention, CPU and I/O.
7. Use read-only credentials, per-statement timeout, total job timeout, cancellation and row budget.
8. Evaluate restored fixture against a fresh schema and check the exact defect signature.

**Note:** Synthetic local benchmark numbers are not predictions of production replica load.
