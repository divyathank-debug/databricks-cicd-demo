# Databricks notebook source

df = spark.read.option("header", "true").csv(
    "abfss://ctms-landing@pfizerclinicaldata.dfs.core.windows.net/study_master/"
)
display(df)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM clinical.bronze.study_master;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM clinical.silver.study_master;
