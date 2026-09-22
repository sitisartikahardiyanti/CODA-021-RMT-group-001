CREATE SCHEMA IF NOT EXISTS job_salary;

DROP TABLE IF EXISTS job_salary.fact_salary CASCADE;
DROP TABLE IF EXISTS job_salary.dim_job CASCADE;
DROP TABLE IF EXISTS job_salary.dim_company CASCADE;
DROP TABLE IF EXISTS job_salary.dim_location CASCADE;


-- ==============================
-- DIM JOB
-- ==============================

CREATE TABLE job_salary.dim_job (

    job_id SERIAL PRIMARY KEY,

    job_title VARCHAR(255) NOT NULL,

    job_category VARCHAR(100) NOT NULL,

    UNIQUE(job_title, job_category)

);


-- ==============================
-- DIM COMPANY
-- ==============================

CREATE TABLE job_salary.dim_company (

    company_id SERIAL PRIMARY KEY,

    company_name VARCHAR(255) NOT NULL UNIQUE

);


-- ==============================
-- DIM LOCATION
-- ==============================

CREATE TABLE job_salary.dim_location (

    location_id SERIAL PRIMARY KEY,

    location_name VARCHAR(255) NOT NULL UNIQUE

);


-- ==============================
-- FACT SALARY
-- ==============================

CREATE TABLE job_salary.fact_salary (

    salary_id SERIAL PRIMARY KEY,

    job_id INTEGER NOT NULL,

    company_id INTEGER NOT NULL,

    location_id INTEGER NOT NULL,

    average_salary NUMERIC(15,2) NOT NULL,

    FOREIGN KEY (job_id)
        REFERENCES job_salary.dim_job(job_id),

    FOREIGN KEY (company_id)
        REFERENCES job_salary.dim_company(company_id),

    FOREIGN KEY (location_id)
        REFERENCES job_salary.dim_location(location_id),

    CHECK (average_salary > 0)

);