-- Databricks notebook source
CREATE EXTERNAL LOCATION `ext_clinical-bronze` URL 'abfss://clinical-bronze@pfizerclinicaldata.dfs.core.windows.net' WITH (STORAGE CREDENTIAL `pfizerclinicaldata_access_cred`);

-- COMMAND ----------

DESCRIBE EXTERNAL LOCATION `ext_clinical-bronze`;

-- COMMAND ----------

CREATE EXTERNAL LOCATION `ext_ctms-landing` URL 'abfss://ctms-landing@pfizerclinicaldata.dfs.core.windows.net' WITH (STORAGE CREDENTIAL `pfizerclinicaldata_access_cred`);

-- COMMAND ----------

LIST 'abfss://ctms-landing@pfizerclinicaldata.dfs.core.windows.net/'

-- COMMAND ----------

CREATE EXTERNAL LOCATION `ext_clinical-silver` URL 'abfss://clinical-silver@pfizerclinicaldata.dfs.core.windows.net' WITH (STORAGE CREDENTIAL `pfizerclinicaldata_access_cred`);

-- COMMAND ----------

CREATE EXTERNAL LOCATION `ext_clinical-gold` URL 'abfss://clinical-gold@pfizerclinicaldata.dfs.core.windows.net' WITH (STORAGE CREDENTIAL `pfizerclinicaldata_access_cred`);
