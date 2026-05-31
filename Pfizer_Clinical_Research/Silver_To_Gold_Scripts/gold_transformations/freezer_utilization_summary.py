# Databricks notebook source
# MAGIC %sql
# MAGIC -- Databricks SQL Notebook
# MAGIC
# MAGIC -- =====================================================
# MAGIC -- GOLD LAYER
# MAGIC -- FREEZER UTILIZATION SUMMARY
# MAGIC --
# MAGIC -- PURPOSE:
# MAGIC -- Biobank freezer capacity and utilization monitoring
# MAGIC --
# MAGIC -- BUSINESS USE CASES:
# MAGIC -- 1. Freezer capacity tracking
# MAGIC -- 2. Storage optimization
# MAGIC -- 3. Empty slot monitoring
# MAGIC -- 4. Cold storage operational reporting
# MAGIC -- 5. Biobank utilization analytics
# MAGIC -- =====================================================
# MAGIC
# MAGIC -- COMMAND ----------
# MAGIC
# MAGIC CREATE OR REPLACE TABLE clinical.gold.freezer_utilization_summary AS
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     f.freezer_id,
# MAGIC
# MAGIC     f.freezer_name,
# MAGIC
# MAGIC     f.freezer_type,
# MAGIC
# MAGIC     f.location,
# MAGIC
# MAGIC     COUNT(DISTINCT r.rack_id) AS total_racks,
# MAGIC
# MAGIC     COUNT(DISTINCT b.box_id) AS total_boxes,
# MAGIC
# MAGIC     COUNT(DISTINCT p.position_id) AS total_positions,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN p.is_occupied = 'Yes'
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS occupied_positions,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN p.is_occupied = 'No'
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS available_positions,
# MAGIC
# MAGIC     ROUND(
# MAGIC         (
# MAGIC             SUM(
# MAGIC                 CASE
# MAGIC                     WHEN p.is_occupied = 'Yes'
# MAGIC                     THEN 1
# MAGIC                     ELSE 0
# MAGIC                 END
# MAGIC             ) * 100.0
# MAGIC         )
# MAGIC         /
# MAGIC         NULLIF(COUNT(DISTINCT p.position_id), 0),
# MAGIC         2
# MAGIC     ) AS utilization_percent,
# MAGIC
# MAGIC     CASE
# MAGIC
# MAGIC         WHEN ROUND(
# MAGIC                 (
# MAGIC                     SUM(
# MAGIC                         CASE
# MAGIC                             WHEN p.is_occupied = 'Yes'
# MAGIC                             THEN 1
# MAGIC                             ELSE 0
# MAGIC                         END
# MAGIC                     ) * 100.0
# MAGIC                 )
# MAGIC                 /
# MAGIC                 NULLIF(COUNT(DISTINCT p.position_id), 0),
# MAGIC                 2
# MAGIC              ) >= 90
# MAGIC         THEN 'CRITICAL'
# MAGIC
# MAGIC         WHEN ROUND(
# MAGIC                 (
# MAGIC                     SUM(
# MAGIC                         CASE
# MAGIC                             WHEN p.is_occupied = 'Yes'
# MAGIC                             THEN 1
# MAGIC                             ELSE 0
# MAGIC                         END
# MAGIC                     ) * 100.0
# MAGIC                 )
# MAGIC                 /
# MAGIC                 NULLIF(COUNT(DISTINCT p.position_id), 0),
# MAGIC                 2
# MAGIC              ) BETWEEN 70 AND 89
# MAGIC         THEN 'HIGH_UTILIZATION'
# MAGIC
# MAGIC         ELSE 'NORMAL'
# MAGIC
# MAGIC     END AS utilization_status,
# MAGIC
# MAGIC     current_timestamp() AS gold_insert_timestamp
# MAGIC
# MAGIC FROM clinical.silver.freezer f
# MAGIC
# MAGIC LEFT JOIN clinical.silver.rack r
# MAGIC     ON f.freezer_id = r.freezer_id
# MAGIC
# MAGIC LEFT JOIN clinical.silver.storage_box b
# MAGIC     ON r.rack_id = b.rack_id
# MAGIC
# MAGIC LEFT JOIN clinical.silver.storage_position p
# MAGIC     ON b.box_id = p.box_id
# MAGIC
# MAGIC GROUP BY
# MAGIC
# MAGIC     f.freezer_id,
# MAGIC
# MAGIC     f.freezer_name,
# MAGIC
# MAGIC     f.freezer_type,
# MAGIC
# MAGIC     f.location;
# MAGIC
# MAGIC

# COMMAND ----------

count = spark.sql("""
SELECT COUNT(*) AS cnt
FROM clinical.gold.freezer_utilization_summary
""").collect()[0]["cnt"]

dbutils.notebook.exit(str(count))
