-- Databricks notebook source
-- Databricks SQL Notebook

-- =====================================================
-- GOLD LAYER
-- SAMPLE TRACKING SUMMARY
--
-- PURPOSE:
-- End-to-end sample lifecycle tracking
--
-- BUSINESS USE CASES:
-- 1. Sample traceability
-- 2. Missing sample detection
-- 3. Accession SLA monitoring
-- 4. Shipment audit tracking
-- 5. Regulatory audit readiness
-- =====================================================

-- COMMAND ----------

CREATE OR REPLACE TABLE clinical.gold.sample_tracking_summary AS

WITH latest_location AS (

    SELECT *
    FROM (

        SELECT
            l.*,

            ROW_NUMBER() OVER (
                PARTITION BY l.sample_id
                ORDER BY l.event_datetime DESC
            ) AS rn

        FROM clinical.silver.lims_sample_location l

    )

    WHERE rn = 1
),

latest_accession AS (

    SELECT *
    FROM (

        SELECT
            a.*,

            ROW_NUMBER() OVER (
                PARTITION BY a.sample_id
                ORDER BY a.accession_datetime DESC
            ) AS rn

        FROM clinical.silver.accession a

    )

    WHERE rn = 1
)

SELECT

    s.sample_id,
    s.sample_barcode,
  
    s.subject_id,
    s.visit_code,
    s.sample_type,
    s.collection_datetime,
    s.received_datetime,
    s.sample_status,
    s.lab_id,

    a.accession_id,
    a.accession_datetime,
    a.accession_status,

    l.storage_location,
    l.event_type AS latest_location_event,
    l.event_datetime AS latest_location_event_time,

    CASE

        WHEN s.received_datetime IS NULL
        THEN 'NOT_RECEIVED'

        WHEN a.accession_id IS NULL
        THEN 'RECEIVED_NOT_ACCESSIONED'

        WHEN s.sample_status = 'Rejected'
        THEN 'REJECTED'

        WHEN s.sample_status = 'Lost'
        THEN 'LOST'

        ELSE 'TRACKED'

    END AS sample_tracking_status,

    current_timestamp() AS gold_insert_timestamp

FROM clinical.silver.lims_sample s

LEFT JOIN latest_accession a
    ON s.sample_id = a.sample_id

LEFT JOIN latest_location l
    ON s.sample_id = l.sample_id;

-- COMMAND ----------

SELECT
    COUNT(*) AS total_records
FROM clinical.gold.sample_tracking_summary;
