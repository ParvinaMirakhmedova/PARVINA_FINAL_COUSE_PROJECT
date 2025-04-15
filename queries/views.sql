
CREATE OR REPLACE VIEW view1_patients_1 AS
SELECT 
    p.patient_ID,
    p.age,
    p.sex,
    p.occupation,
    p.address,
    d.dm_type,
    d.renal_function,
    d.duration,
    d.diabetic_retinopathy,
    d.fbg,
    d.hereditary,
    ds.neuropathy,
    ds.nephropathy,
    ds.smoking,
    ds.bmi
FROM patients_1 p
LEFT JOIN diabetic_retinopathy_1 d ON p.patient_ID = d.patient_ID
LEFT JOIN diseases_1 ds ON p.patient_ID = ds.patient_ID;
