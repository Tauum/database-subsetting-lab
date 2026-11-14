-- Run on a disposable synthetic database ONLY. Adds 10,000 independent process/application pairs.
INSERT INTO process_instance(id,organisation_id,state,status)
SELECT 200000+g,1,jsonb_build_object('submittedDate','2026-11-01','phase','COMPLETE'),'COMPLETE'
FROM generate_series(1,10000) g ON CONFLICT DO NOTHING;
INSERT INTO application(id,process_id,applicant_name)
SELECT 300000+g,200000+g,'Synthetic Applicant '||g
FROM generate_series(1,10000) g ON CONFLICT DO NOTHING;
ANALYZE;
