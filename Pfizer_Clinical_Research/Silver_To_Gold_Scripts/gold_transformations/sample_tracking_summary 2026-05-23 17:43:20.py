# Databricks notebook source
# MAGIC %sql
# MAGIC -- Databricks SQL Notebook
# MAGIC
# MAGIC -- =====================================================
# MAGIC -- GOLD LAYER
# MAGIC -- SAMPLE TRACKING SUMMARY
# MAGIC --
# MAGIC -- PURPOSE:
# MAGIC -- End-to-end sample lifecycle tracking
# MAGIC --
# MAGIC -- BUSINESS USE CASES:
# MAGIC -- 1. Sample traceability
# MAGIC -- 2. Missing sample detection
# MAGIC -- 3. Accession SLA monitoring
# MAGIC -- 4. Shipment audit tracking
# MAGIC -- 5. Regulatory audit readiness
# MAGIC -- =====================================================
# MAGIC
# MAGIC -- COMMAND ----------
# MAGIC
# MAGIC CREATE OR REPLACE TABLE clinical.gold.sample_tracking_summary AS
# MAGIC
# MAGIC WITH latest_location AS (
# MAGIC
# MAGIC     SELECT *
# MAGIC     FROM (
# MAGIC
# MAGIC         SELECT
# MAGIC             l.*,
# MAGIC
# MAGIC             ROW_NUMBER() OVER (
# MAGIC                 PARTITION BY l.sample_id
# MAGIC                 ORDER BY l.event_datetime DESC
# MAGIC             ) AS rn
# MAGIC
# MAGIC         FROM clinical.silver.lims_sample_location l
# MAGIC
# MAGIC     )
# MAGIC
# MAGIC     WHERE rn = 1
# MAGIC ),
# MAGIC
# MAGIC latest_accession AS (
# MAGIC
# MAGIC     SELECT *
# MAGIC     FROM (
# MAGIC
# MAGIC         SELECT
# MAGIC             a.*,
# MAGIC
# MAGIC             ROW_NUMBER() OVER (
# MAGIC                 PARTITION BY a.sample_id
# MAGIC                 ORDER BY a.accession_datetime DESC
# MAGIC             ) AS rn
# MAGIC
# MAGIC         FROM clinical.silver.accession a
# MAGIC
# MAGIC     )
# MAGIC
# MAGIC     WHERE rn = 1
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     s.sample_id,
# MAGIC     s.sample_barcode,
# MAGIC     s.study_id,
# MAGIC     s.subject_id,
# MAGIC     s.visit_code,
# MAGIC     s.sample_type,
# MAGIC     s.collection_datetime,
# MAGIC     s.received_datetime,
# MAGIC     s.sample_status,
# MAGIC     s.lab_id,
# MAGIC
# MAGIC     a.accession_id,
# MAGIC     a.accession_datetime,
# MAGIC     a.accession_status,
# MAGIC
# MAGIC     l.storage_location,
# MAGIC     l.event_type AS latest_location_event,
# MAGIC     l.event_datetime AS latest_location_event_time,
# MAGIC
# MAGIC     CASE
# MAGIC
# MAGIC         WHEN s.received_datetime IS NULL
# MAGIC         THEN 'NOT_RECEIVED'
# MAGIC
# MAGIC         WHEN a.accession_id IS NULL
# MAGIC         THEN 'RECEIVED_NOT_ACCESSIONED'
# MAGIC
# MAGIC         WHEN s.sample_status = 'Rejected'
# MAGIC         THEN 'REJECTED'
# MAGIC
# MAGIC         WHEN s.sample_status = 'Lost'
# MAGIC         THEN 'LOST'
# MAGIC
# MAGIC         ELSE 'TRACKED'
# MAGIC
# MAGIC     END AS sample_tracking_status,
# MAGIC
# MAGIC     current_timestamp() AS gold_insert_timestamp
# MAGIC
# MAGIC FROM clinical.silver.lims_sample s
# MAGIC
# MAGIC LEFT JOIN latest_accession a
# MAGIC     ON s.sample_id = a.sample_id
# MAGIC
# MAGIC LEFT JOIN latest_location l
# MAGIC     ON s.sample_id = l.sample_id;
# MAGIC
# MAGIC

# COMMAND ----------

count = spark.sql("""
SELECT COUNT(*) AS cnt
FROM clinical.gold.sample_tracking_summary
""").collect()[0]["cnt"]

dbutils.notebook.exit(str(count))
