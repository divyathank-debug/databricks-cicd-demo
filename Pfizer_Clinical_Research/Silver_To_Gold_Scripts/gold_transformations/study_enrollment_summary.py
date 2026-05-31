# Databricks notebook source
# MAGIC %sql
# MAGIC -- Databricks SQL Notebook
# MAGIC
# MAGIC -- =====================================================
# MAGIC -- GOLD LAYER
# MAGIC -- STUDY ENROLLMENT SUMMARY
# MAGIC --
# MAGIC -- PURPOSE:
# MAGIC -- Clinical study enrollment KPI aggregation
# MAGIC --
# MAGIC -- BUSINESS USE CASES:
# MAGIC -- 1. Study enrollment monitoring
# MAGIC -- 2. Screening failure analysis
# MAGIC -- 3. Region-wise enrollment tracking
# MAGIC -- 4. Study progress reporting
# MAGIC -- 5. Operational dashboarding
# MAGIC -- =====================================================
# MAGIC
# MAGIC -- COMMAND ----------
# MAGIC
# MAGIC CREATE OR REPLACE TABLE clinical.gold.study_enrollment_summary AS
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     sm.study_id,
# MAGIC
# MAGIC     sm.study_name,
# MAGIC
# MAGIC     sm.phase,
# MAGIC
# MAGIC     sm.therapeutic_area,
# MAGIC
# MAGIC     sm.region,
# MAGIC
# MAGIC     sm.protocol_version,
# MAGIC
# MAGIC     COUNT(DISTINCT s.subject_id) AS total_subjects,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN s.enrollment_status = 'Enrolled'
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS enrolled_subjects,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN s.enrollment_status = 'Screen Failed'
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS screen_failed_subjects,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN s.enrollment_status = 'Withdrawn'
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS withdrawn_subjects,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN s.enrollment_status = 'Completed'
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS completed_subjects,
# MAGIC
# MAGIC     ROUND(
# MAGIC         (
# MAGIC             SUM(
# MAGIC                 CASE
# MAGIC                     WHEN s.enrollment_status = 'Enrolled'
# MAGIC                     THEN 1
# MAGIC                     ELSE 0
# MAGIC                 END
# MAGIC             ) * 100.0
# MAGIC         )
# MAGIC         /
# MAGIC         NULLIF(COUNT(DISTINCT s.subject_id), 0),
# MAGIC         2
# MAGIC     ) AS enrollment_rate_percent,
# MAGIC
# MAGIC     ROUND(
# MAGIC         (
# MAGIC             SUM(
# MAGIC                 CASE
# MAGIC                     WHEN s.enrollment_status = 'Screen Failed'
# MAGIC                     THEN 1
# MAGIC                     ELSE 0
# MAGIC                 END
# MAGIC             ) * 100.0
# MAGIC         )
# MAGIC         /
# MAGIC         NULLIF(COUNT(DISTINCT s.subject_id), 0),
# MAGIC         2
# MAGIC     ) AS screen_failure_rate_percent,
# MAGIC
# MAGIC     MIN(s.enrollment_date) AS first_enrollment_date,
# MAGIC
# MAGIC     MAX(s.enrollment_date) AS latest_enrollment_date,
# MAGIC
# MAGIC     current_timestamp() AS gold_insert_timestamp
# MAGIC
# MAGIC FROM clinical.silver.study_master sm
# MAGIC
# MAGIC LEFT JOIN clinical.silver.subject s
# MAGIC     ON sm.study_id = s.study_id
# MAGIC
# MAGIC GROUP BY
# MAGIC
# MAGIC     sm.study_id,
# MAGIC
# MAGIC     sm.study_name,
# MAGIC
# MAGIC     sm.phase,
# MAGIC
# MAGIC     sm.therapeutic_area,
# MAGIC
# MAGIC     sm.region,
# MAGIC
# MAGIC     sm.protocol_version;

# COMMAND ----------


count = spark.sql("""
SELECT COUNT(*) AS cnt
FROM clinical.gold.study_enrollment_summary
""").collect()[0]["cnt"]

dbutils.notebook.exit(str(count))
