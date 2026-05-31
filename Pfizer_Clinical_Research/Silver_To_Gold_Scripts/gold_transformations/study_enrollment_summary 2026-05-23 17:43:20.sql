-- Databricks notebook source
-- Databricks SQL Notebook

-- =====================================================
-- GOLD LAYER
-- STUDY ENROLLMENT SUMMARY
--
-- PURPOSE:
-- Clinical study enrollment KPI aggregation
--
-- BUSINESS USE CASES:
-- 1. Study enrollment monitoring
-- 2. Screening failure analysis
-- 3. Region-wise enrollment tracking
-- 4. Study progress reporting
-- 5. Operational dashboarding
-- =====================================================

-- COMMAND ----------

CREATE OR REPLACE TABLE clinical.gold.study_enrollment_summary AS

SELECT

    sm.study_id,

    sm.study_name,

    sm.phase,

    sm.therapeutic_area,

    sm.region,

    sm.protocol_version,

    COUNT(DISTINCT s.subject_id) AS total_subjects,

    SUM(
        CASE
            WHEN s.enrollment_status = 'Enrolled'
            THEN 1
            ELSE 0
        END
    ) AS enrolled_subjects,

    SUM(
        CASE
            WHEN s.enrollment_status = 'Screen Failed'
            THEN 1
            ELSE 0
        END
    ) AS screen_failed_subjects,

    SUM(
        CASE
            WHEN s.enrollment_status = 'Withdrawn'
            THEN 1
            ELSE 0
        END
    ) AS withdrawn_subjects,

    SUM(
        CASE
            WHEN s.enrollment_status = 'Completed'
            THEN 1
            ELSE 0
        END
    ) AS completed_subjects,

    ROUND(
        (
            SUM(
                CASE
                    WHEN s.enrollment_status = 'Enrolled'
                    THEN 1
                    ELSE 0
                END
            ) * 100.0
        )
        /
        NULLIF(COUNT(DISTINCT s.subject_id), 0),
        2
    ) AS enrollment_rate_percent,

    ROUND(
        (
            SUM(
                CASE
                    WHEN s.enrollment_status = 'Screen Failed'
                    THEN 1
                    ELSE 0
                END
            ) * 100.0
        )
        /
        NULLIF(COUNT(DISTINCT s.subject_id), 0),
        2
    ) AS screen_failure_rate_percent,

    MIN(s.enrollment_date) AS first_enrollment_date,

    MAX(s.enrollment_date) AS latest_enrollment_date,

    current_timestamp() AS gold_insert_timestamp

FROM clinical.silver.study_master sm

LEFT JOIN clinical.silver.subject s
    ON sm.study_id = s.study_id

GROUP BY

    sm.study_id,

    sm.study_name,

    sm.phase,

    sm.therapeutic_area,

    sm.region,

    sm.protocol_version;

-- COMMAND ----------

SELECT
    COUNT(*) AS total_records
FROM clinical.gold.study_enrollment_summary;
