-- Databricks notebook source
-- Databricks SQL Notebook

-- =====================================================
-- GOLD LAYER
-- SHIPMENT SLA SUMMARY
--
-- PURPOSE:
-- Shipment delivery SLA monitoring
--
-- BUSINESS USE CASES:
-- 1. Shipment tracking
-- 2. SLA breach analysis
-- 3. Courier performance monitoring
-- 4. Cold-chain logistics monitoring
-- 5. Delayed shipment investigation
-- =====================================================

-- COMMAND ----------

CREATE OR REPLACE TABLE clinical.gold.shipment_sla_summary AS

SELECT

    sh.shipment_id,

    sh.shipment_type,

    sh.plant_code,

    sh.source_location,

    sh.destination_location,

    sh.carrier_id,

    sh.tracking_number,

    sh.shipment_datetime,

    dh.actual_delivery_datetime,

    COUNT(DISTINCT si.item_id) AS total_items,

    ROUND(
        TIMESTAMPDIFF(
            HOUR,
            sh.shipment_datetime,
            dh.actual_delivery_datetime
        ),
        2
    ) AS delivery_duration_hours,

    CASE

        WHEN dh.actual_delivery_datetime IS NULL
        THEN 'IN_TRANSIT'

        WHEN TIMESTAMPDIFF(
                HOUR,
                sh.shipment_datetime,
                dh.actual_delivery_datetime
             ) <= 48
        THEN 'WITHIN_SLA'

        ELSE 'SLA_BREACHED'

    END AS sla_status,

    CASE

        WHEN TIMESTAMPDIFF(
                HOUR,
                sh.shipment_datetime,
                dh.actual_delivery_datetime
             ) <= 24
        THEN 'FAST_DELIVERY'

        WHEN TIMESTAMPDIFF(
                HOUR,
                sh.shipment_datetime,
                dh.actual_delivery_datetime
             ) BETWEEN 25 AND 48
        THEN 'NORMAL_DELIVERY'

        ELSE 'DELAYED_DELIVERY'

    END AS shipment_performance_category,

    current_timestamp() AS gold_insert_timestamp

FROM clinical.silver.shipment_header sh

LEFT JOIN clinical.silver.shipment_item si
    ON sh.shipment_id = si.shipment_id

LEFT JOIN clinical.silver.delivery_header dh
    ON sh.shipment_id = dh.shipment_id

GROUP BY

    sh.shipment_id,

    sh.shipment_type,

    sh.plant_code,

    sh.source_location,

    sh.destination_location,

    sh.carrier_id,

    sh.tracking_number,

    sh.shipment_datetime,

    dh.actual_delivery_datetime;

-- COMMAND ----------

SELECT
    COUNT(*) AS total_records
FROM clinical.gold.shipment_sla_summary;
