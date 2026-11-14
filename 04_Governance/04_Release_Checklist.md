# Restricted-to-developer release checklist
- Source approved and extraction logged.
- Rows and relationships checked against defect description.
- Invalid state and orphan scenarios intentionally preserved.
- Direct identifiers, free text, JSONB and history payloads inspected.
- Re-identification risk assessed by authorised privacy reviewer; approval documented.
- Restore tested on isolated environment with matching schema.
- Fixture encrypted in transit and at rest, recipient access scoped, retention and deletion recorded.
- Reviewers and version of masking rules recorded.
If any item fails, do not distribute the fixture.
