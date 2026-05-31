-- Databricks notebook source
-- Databricks SQL Notebook

-- =====================================================
-- GOLD LAYER
-- FREEZER UTILIZATION SUMMARY
--
-- PURPOSE:
-- Biobank freezer capacity and utilization monitoring
--
-- BUSINESS USE CASES:
-- 1. Freezer capacity tracking
-- 2. Storage optimization
-- 3. Empty slot monitoring
-- 4. Cold storage operational reporting
-- 5. Biobank utilization analytics
-- =====================================================

-- COMMAND ----------

CREATE OR REPLACE TABLE clinical.gold.freezer_utilization_summary AS

SELECT

    f.freezer_id,

    f.freezer_name,

    f.freezer_type,

    f.location,

    COUNT(DISTINCT r.rack_id) AS total_racks,

    COUNT(DISTINCT b.box_id) AS total_boxes,

    COUNT(DISTINCT p.position_id) AS total_positions,

    SUM(
        CASE
            WHEN p.is_occupied = 'Yes'
            THEN 1
            ELSE 0
        END
    ) AS occupied_positions,

    SUM(
        CASE
            WHEN p.is_occupied = 'No'
            THEN 1
            ELSE 0
        END
    ) AS available_positions,

    ROUND(
        (
            SUM(
                CASE
                    WHEN p.is_occupied = 'Yes'
                    THEN 1
                    ELSE 0
                END
            ) * 100.0
        )
        /
        NULLIF(COUNT(DISTINCT p.position_id), 0),
        2
    ) AS utilization_percent,

    CASE

        WHEN ROUND(
                (
                    SUM(
                        CASE
                            WHEN p.is_occupied = 'Yes'
                            THEN 1
                            ELSE 0
                        END
                    ) * 100.0
                )
                /
                NULLIF(COUNT(DISTINCT p.position_id), 0),
                2
             ) >= 90
        THEN 'CRITICAL'

        WHEN ROUND(
                (
                    SUM(
                        CASE
                            WHEN p.is_occupied = 'Yes'
                            THEN 1
                            ELSE 0
                        END
                    ) * 100.0
                )
                /
                NULLIF(COUNT(DISTINCT p.position_id), 0),
                2
             ) BETWEEN 70 AND 89
        THEN 'HIGH_UTILIZATION'

        ELSE 'NORMAL'

    END AS utilization_status,

    current_timestamp() AS gold_insert_timestamp

FROM clinical.silver.freezer f

LEFT JOIN clinical.silver.rack r
    ON f.freezer_id = r.freezer_id

LEFT JOIN clinical.silver.storage_box b
    ON r.rack_id = b.rack_id

LEFT JOIN clinical.silver.storage_position p
    ON b.box_id = p.box_id

GROUP BY

    f.freezer_id,

    f.freezer_name,

    f.freezer_type,

    f.location;

-- COMMAND ----------

SELECT
    COUNT(*) AS total_records
FROM clinical.gold.freezer_utilization_summary;
