DROP TABLE IF EXISTS patients_1;
CREATE TABLE patients_1 (
    patient_ID INTEGER PRIMARY KEY,
    full_name TEXT,
    age INTEGER,
    sex TEXT,
    occupation TEXT,
    address TEXT
);

DROP TABLE IF EXISTS diabetic_retinopathy_1;
CREATE TABLE diabetic_retinopathy_1 (
    patient_ID INTEGER PRIMARY KEY,
    full_name TEXT,
    dm_type TEXT,
    renal_function TEXT,
    duration INTEGER,
    diabetic_retinopathy TEXT,
    fbg DOUBLE,
    hereditary TEXT,
    FOREIGN KEY (patient_ID) REFERENCES patients_1 (patient_ID)
);

DROP TABLE IF EXISTS diseases_1;
CREATE TABLE diseases_1 (
    patient_ID INTEGER PRIMARY KEY,
    neuropathy TEXT,
    nephropathy TEXT,
    smoking TEXT,
    bmi DOUBLE,
    FOREIGN KEY (patient_ID) REFERENCES patients_1 (patient_ID)
);