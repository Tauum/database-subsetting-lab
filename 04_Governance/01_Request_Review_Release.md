# Operational workstream and privacy gates

## Request fields
Defect ID; source environment; root table; root ID; observed error/signature; relevant timestamp; schema/app version; priority; requester; permitted reviewers.

## Status
Requested → Approved for extraction → Queued → Extracted (restricted) → Technical review → Privacy review → Released → Restored and reproduced → Archived/deleted.

## Responsibilities
- Developer: identify failure, provide root key and expected signature; verify reproduction locally.
- SQL expert: review extraction scope, relationship coverage, restore integrity and technical fidelity; not required to hand-build all records.
- Privacy/security approver: decide lawful processing, transfer and anonymisation criteria; approve release.
- Operator: schedule bounded jobs, monitor read replica, securely store and expire artifacts.

## Restricted processing
Raw extraction remains in an approved environment. Masking and review occur before distribution. Pseudonymised data may still be personal data. A human sign-off does not by itself prove anonymisation. Track access, retention, deletion, and onward distribution.

## Handoff artifact
Defect ID; schema version; extraction root; included tables/row counts; excluded relationships; masking policy version; privacy approval; SHA-256 checksum; restore command; reproduction steps; expected error; expiration date.

## Stop conditions
Query exceeds duration/row budget; replica lag exceeds threshold; unexpected tables appear; sensitive fields remain; failure signature is lost; restore or integrity checks fail.
