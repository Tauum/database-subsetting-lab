# Masking test matrix
| Field | Expected | Defect constraint |
|---|---|---|
| organisation.contact_email | Synthetic replacement | Preserve valid email syntax |
| participant.email | Deterministic synthetic email | No real value leaks |
| application.applicant_name | Synthetic name | Do not alter foreign keys |
| attachment_metadata.metadata.ownerEmail | Mask nested JSONB | Preserve JSON structure |
| process_instance.state.submittedDate | Keep `31/99/2026` | Required failure signature |
| process_instance.state.embeddedParticipantId | Stable mapped ID or unchanged synthetic ID | Keep relationship |
| comment.body | Review for PII/free text | Do not silently remove defect |
Approval requires field inventory, direct identifiers check, quasi-identifier review and explicit reviewer sign-off. This is a test matrix, not a GDPR certification.
