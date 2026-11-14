# Jailer: limits and validation

## Traversal
No known fixed five-level traversal ceiling; recursion depends on associations configured in the extraction model. Missing FK declarations, restricted associations, JSON references, and missing parent rows cause incomplete coverage. Shared parents can cause expansion into unrelated children.

## Performance safeguards
Prefer a read replica. Use a read-only role, `statement_timeout`, connection limits, job-level timeout, row-count threshold, sequential jobs, and replica lag monitoring. A SQL statement timeout alone does not cap a whole extraction job.

## Test checklist
- [ ] 10-level chain, every row retained
- [ ] Two branches with shared parent; no unrelated sibling process
- [ ] Cyclic nullable association handled
- [ ] All required history rows included
- [ ] JSONB implicit references identified or explicitly documented
- [ ] Broken logical parent reference preserved
- [ ] Generated SQL restores to clean schema
- [ ] Repeatability of extracted row set
- [ ] Record extraction duration, query count, rows and replica lag
- [ ] Sensitive values are not released in exported fixture

## Go/no-go
No-go if extracting a single case requires hours of manual relationship repair or if it loses the defect signature.
