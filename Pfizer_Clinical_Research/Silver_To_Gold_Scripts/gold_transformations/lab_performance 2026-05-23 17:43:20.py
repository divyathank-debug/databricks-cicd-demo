# Databricks notebook source
# MAGIC %sql
# MAGIC -- Databricks SQL Notebook
# MAGIC
# MAGIC -- =====================================================
# MAGIC -- GOLD LAYER
# MAGIC -- LAB PERFORMANCE SUMMARY
# MAGIC --
# MAGIC -- PURPOSE:
# MAGIC -- Lab operational KPI aggregation
# MAGIC --
# MAGIC -- BUSINESS USE CASES:
# MAGIC -- 1. Lab turnaround SLA tracking
# MAGIC -- 2. Critical result monitoring
# MAGIC -- 3. Abnormal result trend analysis
# MAGIC -- 4. Lab workload measurement
# MAGIC -- 5. Operational performance dashboarding
# MAGIC -- =====================================================
# MAGIC
# MAGIC -- COMMAND ----------
# MAGIC
# MAGIC CREATE OR REPLACE TABLE clinical.gold.lab_performance AS
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     s.lab_id,
# MAGIC
# MAGIC     COUNT(DISTINCT s.sample_id) AS total_samples,
# MAGIC
# MAGIC     COUNT(DISTINCT a.accession_id) AS total_accessions,
# MAGIC
# MAGIC     COUNT(DISTINCT an.analysis_id) AS total_analyses,
# MAGIC
# MAGIC     COUNT(DISTINCT r.result_id) AS total_results,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN r.result_status = 'Final'
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS final_results,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN r.abnormal_flag = 'YES'
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS abnormal_results,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN r.critical_flag = 'YES'
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS critical_results,
# MAGIC
# MAGIC     ROUND(
# MAGIC         AVG(
# MAGIC             TIMESTAMPDIFF(
# MAGIC                 HOUR,
# MAGIC                 s.received_datetime,
# MAGIC                 r.result_datetime
# MAGIC             )
# MAGIC         ),
# MAGIC         2
# MAGIC     ) AS avg_turnaround_hours,
# MAGIC
# MAGIC     MIN(r.result_datetime) AS first_result_datetime,
# MAGIC
# MAGIC     MAX(r.result_datetime) AS latest_result_datetime,
# MAGIC
# MAGIC     current_timestamp() AS gold_insert_timestamp
# MAGIC
# MAGIC FROM clinical.silver.lims_sample s
# MAGIC
# MAGIC LEFT JOIN clinical.silver.accession a
# MAGIC     ON s.sample_id = a.sample_id
# MAGIC
# MAGIC LEFT JOIN clinical.silver.analysis an
# MAGIC     ON a.accession_id = an.accession_id
# MAGIC
# MAGIC LEFT JOIN clinical.silver.result r
# MAGIC     ON an.analysis_id = r.analysis_id
# MAGIC
# MAGIC GROUP BY
# MAGIC     s.lab_id;
# MAGIC
# MAGIC

# COMMAND ----------

count = spark.sql("""
SELECT COUNT(*) AS cnt
FROM clinical.gold.lab_performance
""").collect()[0]["cnt"]

dbutils.notebook.exit(str(count))
