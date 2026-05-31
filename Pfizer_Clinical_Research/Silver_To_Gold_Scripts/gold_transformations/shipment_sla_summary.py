# Databricks notebook source
# MAGIC %sql
# MAGIC -- Databricks SQL Notebook
# MAGIC
# MAGIC -- =====================================================
# MAGIC -- GOLD LAYER
# MAGIC -- SHIPMENT SLA SUMMARY
# MAGIC --
# MAGIC -- PURPOSE:
# MAGIC -- Shipment delivery SLA monitoring
# MAGIC --
# MAGIC -- BUSINESS USE CASES:
# MAGIC -- 1. Shipment tracking
# MAGIC -- 2. SLA breach analysis
# MAGIC -- 3. Courier performance monitoring
# MAGIC -- 4. Cold-chain logistics monitoring
# MAGIC -- 5. Delayed shipment investigation
# MAGIC -- =====================================================
# MAGIC
# MAGIC -- COMMAND ----------
# MAGIC
# MAGIC CREATE OR REPLACE TABLE clinical.gold.shipment_sla_summary AS
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     sh.shipment_id,
# MAGIC
# MAGIC     sh.shipment_type,
# MAGIC
# MAGIC     sh.plant_code,
# MAGIC
# MAGIC     sh.source_location,
# MAGIC
# MAGIC     sh.destination_location,
# MAGIC
# MAGIC     sh.carrier_id,
# MAGIC
# MAGIC     sh.tracking_number,
# MAGIC
# MAGIC     sh.shipment_datetime,
# MAGIC
# MAGIC     dh.actual_delivery_datetime,
# MAGIC
# MAGIC     COUNT(DISTINCT si.item_id) AS total_items,
# MAGIC
# MAGIC     ROUND(
# MAGIC         TIMESTAMPDIFF(
# MAGIC             HOUR,
# MAGIC             sh.shipment_datetime,
# MAGIC             dh.actual_delivery_datetime
# MAGIC         ),
# MAGIC         2
# MAGIC     ) AS delivery_duration_hours,
# MAGIC
# MAGIC     CASE
# MAGIC
# MAGIC         WHEN dh.actual_delivery_datetime IS NULL
# MAGIC         THEN 'IN_TRANSIT'
# MAGIC
# MAGIC         WHEN TIMESTAMPDIFF(
# MAGIC                 HOUR,
# MAGIC                 sh.shipment_datetime,
# MAGIC                 dh.actual_delivery_datetime
# MAGIC              ) <= 48
# MAGIC         THEN 'WITHIN_SLA'
# MAGIC
# MAGIC         ELSE 'SLA_BREACHED'
# MAGIC
# MAGIC     END AS sla_status,
# MAGIC
# MAGIC     CASE
# MAGIC
# MAGIC         WHEN TIMESTAMPDIFF(
# MAGIC                 HOUR,
# MAGIC                 sh.shipment_datetime,
# MAGIC                 dh.actual_delivery_datetime
# MAGIC              ) <= 24
# MAGIC         THEN 'FAST_DELIVERY'
# MAGIC
# MAGIC         WHEN TIMESTAMPDIFF(
# MAGIC                 HOUR,
# MAGIC                 sh.shipment_datetime,
# MAGIC                 dh.actual_delivery_datetime
# MAGIC              ) BETWEEN 25 AND 48
# MAGIC         THEN 'NORMAL_DELIVERY'
# MAGIC
# MAGIC         ELSE 'DELAYED_DELIVERY'
# MAGIC
# MAGIC     END AS shipment_performance_category,
# MAGIC
# MAGIC     current_timestamp() AS gold_insert_timestamp
# MAGIC
# MAGIC FROM clinical.silver.shipment_header sh
# MAGIC
# MAGIC LEFT JOIN clinical.silver.shipment_item si
# MAGIC     ON sh.shipment_id = si.shipment_id
# MAGIC
# MAGIC LEFT JOIN clinical.silver.delivery_header dh
# MAGIC     ON sh.shipment_id = dh.shipment_id
# MAGIC
# MAGIC GROUP BY
# MAGIC
# MAGIC     sh.shipment_id,
# MAGIC
# MAGIC     sh.shipment_type,
# MAGIC
# MAGIC     sh.plant_code,
# MAGIC
# MAGIC     sh.source_location,
# MAGIC
# MAGIC     sh.destination_location,
# MAGIC
# MAGIC     sh.carrier_id,
# MAGIC
# MAGIC     sh.tracking_number,
# MAGIC
# MAGIC     sh.shipment_datetime,
# MAGIC
# MAGIC     dh.actual_delivery_datetime;

# COMMAND ----------


count = spark.sql("""
SELECT COUNT(*) AS cnt
FROM clinical.gold.shipment_sla_summary
""").collect()[0]["cnt"]

dbutils.notebook.exit(str(count))
