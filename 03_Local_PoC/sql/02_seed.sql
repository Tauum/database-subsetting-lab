INSERT INTO organisation VALUES (1,'Example Group','contact@example.invalid');
INSERT INTO process_instance VALUES
(1001,1,'{"submittedDate":"31/99/2026","embeddedParticipantId":3001,"phase":"AWAITING_APPROVAL"}','ACTIVE'),
(1002,1,'{"submittedDate":"2026-11-01","phase":"COMPLETE"}','COMPLETE');
INSERT INTO application VALUES (2001,1001,'Demo Applicant'),(2002,1002,'Other Applicant');
INSERT INTO participant VALUES (3001,2001,NULL,'demo@example.invalid'),(3002,2002,NULL,'other@example.invalid');
INSERT INTO document VALUES (4001,3001,'form.pdf'),(4002,3002,'other.pdf');
INSERT INTO attachment VALUES (5001,4001,'file-1'),(5002,4002,'file-2');
INSERT INTO attachment_metadata VALUES (6001,5001,'{"source":"demo","ownerEmail":"demo@example.invalid"}'),(6002,5002,'{"source":"other"}');
INSERT INTO task VALUES (7001,1001,'{"assignee":"demo@example.invalid","status":"WAITING"}'),(7002,1002,'{"status":"DONE"}');
INSERT INTO approval VALUES (8001,7001,'PENDING'),(8002,7002,'APPROVED');
INSERT INTO comment VALUES (9001,2001,'Demo-only text'),(9002,2002,'Other process');
INSERT INTO process_event VALUES (10001,1001,'{"kind":"START"}'),(10002,1002,'{"kind":"END"}');
INSERT INTO external_reference VALUES (11001,1001,'valid-logical-ref'),(11002,999999,'orphaned-logical-ref');
INSERT INTO organisation_history VALUES (12001,1,'INSERT','{"recordId":1,"event":"created"}');
INSERT INTO process_instance_history VALUES (12002,1001,'INSERT','{"recordId":1001,"event":"created"}');
INSERT INTO application_history VALUES (12003,2001,'INSERT','{"recordId":2001,"event":"created"}');
INSERT INTO participant_history VALUES (12004,3001,'INSERT','{"recordId":3001,"event":"created"}');
INSERT INTO document_history VALUES (12005,4001,'INSERT','{"recordId":4001,"event":"created"}');
INSERT INTO attachment_history VALUES (12006,5001,'INSERT','{"recordId":5001,"event":"created"}');
INSERT INTO attachment_metadata_history VALUES (12007,6001,'INSERT','{"recordId":6001,"event":"created"}');
INSERT INTO task_history VALUES (12008,7001,'INSERT','{"recordId":7001,"event":"created"}');
INSERT INTO approval_history VALUES (12009,8001,'INSERT','{"recordId":8001,"event":"created"}');
INSERT INTO comment_history VALUES (12010,9001,'INSERT','{"recordId":9001,"event":"created"}');
INSERT INTO process_event_history VALUES (12011,10001,'INSERT','{"recordId":10001,"event":"created"}');
INSERT INTO external_reference_history VALUES (12012,11001,'INSERT','{"recordId":11001,"event":"created"}');
