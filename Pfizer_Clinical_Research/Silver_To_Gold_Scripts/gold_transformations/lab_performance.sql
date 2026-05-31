-- Databricks notebook source
-- Databricks SQL Notebook

-- =====================================================
-- GOLD LAYER
-- LAB PERFORMANCE SUMMARY
--
-- PURPOSE:
-- Lab operational KPI aggregation
--
-- BUSINESS USE CASES:
-- 1. Lab turnaround SLA tracking
-- 2. Critical result monitoring
-- 3. Abnormal result trend analysis
-- 4. Lab workload measurement
-- 5. Operational performance dashboarding
-- =====================================================

-- COMMAND ----------

CREATE OR REPLACE TABLE clinical.gold.lab_performance AS

SELECT

    s.lab_id,

    COUNT(DISTINCT s.sample_id) AS total_samples,

    COUNT(DISTINCT a.accession_id) AS total_accessions,

    COUNT(DISTINCT an.analysis_id) AS total_analyses,

    COUNT(DISTINCT r.result_id) AS total_results,

    SUM(
        CASE
            WHEN r.result_status = 'Final'
            THEN 1
            ELSE 0
        END
    ) AS final_results,

    SUM(
        CASE
            WHEN r.abnormal_flag = 'YES'
            THEN 1
            ELSE 0
        END
    ) AS abnormal_results,

    SUM(
        CASE
            WHEN r.critical_flag = 'YES'
            THEN 1
            ELSE 0
        END
    ) AS critical_results,

    ROUND(
        AVG(
            TIMESTAMPDIFF(
                HOUR,
                s.received_datetime,
                r.result_datetime
            )
        ),
        2
    ) AS avg_turnaround_hours,

    MIN(r.result_datetime) AS first_result_datetime,

    MAX(r.result_datetime) AS latest_result_datetime,

    current_timestamp() AS gold_insert_timestamp

FROM clinical.silver.lims_sample s

LEFT JOIN clinical.silver.accession a
    ON s.sample_id = a.sample_id

LEFT JOIN clinical.silver.analysis an
    ON a.accession_id = an.accession_id

LEFT JOIN clinical.silver.result r
    ON an.analysis_id = r.analysis_id

GROUP BY
    s.lab_id;

-- COMMAND ----------

SELECT
    COUNT(*) AS total_records
FROM clinical.gold.lab_performance;
