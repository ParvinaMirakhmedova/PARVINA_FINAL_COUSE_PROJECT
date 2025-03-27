--1. Количество пациентов по полу
SELECT sex, COUNT(*) AS count
FROM view1_patients_1
GROUP BY sex;


--2. Средний возраст по полу
SELECT sex, AVG(age) AS avg_age
FROM view1_patients_1
GROUP BY sex;

--3. Среднее значение BMI по типу диабета
SELECT *
FROM view1_patients_1
WHERE LOWER(neuropathy) = 'yes' AND LOWER(nephropathy) = 'yes';

--4. Пациенты с высоким FBG (>7.0) (или другим порогом)
SELECT *
FROM view1_patients_1
WHERE fbg > 7.0;

-- 5. Распределение типов диабета по полу
SELECT sex, dm_type, COUNT(*) AS count
FROM view1_patients_1
GROUP BY sex, dm_type;

-- 6. BMI и возраст по каждому типу диабета (для scatter-графика)
SELECT dm_type, bmi, age
FROM view1_patients_1
WHERE bmi IS NOT NULL AND age IS NOT NULL;


-- 7.  Пациенты с диабетической ретинопатией
SELECT full_name, dm_type, diabetic_retinopathy
FROM view1_patients_1
WHERE diabetic_retinopathy = 'yes';

-- 8. Пациенты с курением и высоким BMI (>30) (фактор риска)
SELECT full_name, age, bmi, smoking
FROM view1_patients_1
WHERE smoking = 'yes' AND bmi > 30;

