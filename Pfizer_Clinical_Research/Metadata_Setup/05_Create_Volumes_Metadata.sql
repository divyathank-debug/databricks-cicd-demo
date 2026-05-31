-- Databricks notebook source
drop schema if exists clinical.source cascade;

-- COMMAND ----------


-- =====================================================
-- CREATE SOURCE SCHEMA
-- =====================================================

CREATE SCHEMA IF NOT EXISTS clinical.source;

-- COMMAND ----------

-- DROP VOLUME IF EXISTS clinical.source.ctms_volume;

-- COMMAND ----------

-- =====================================================
-- CTMS LANDING EXTERNAL VOLUME
-- =====================================================

CREATE EXTERNAL VOLUME IF NOT EXISTS clinical.source.ctms_volume
LOCATION 'abfss://ctms-landing@pfizerclinicaldat.dfs.core.windows.net/';

-- COMMAND ----------

-- This creates:

-- /Volumes/clinical/source/ctms_volume/

-- which becomes:

-- your filesystem abstraction

-- COMMAND ----------

-- Databricks maps:

-- entire ADLS path 'abfss://ctms-landing@pfizerclinicaldata.dfs.core.windows.net/'

-- to:

-- /Volumes/clinical/source/ctms_volume/


-- SO IF ADLS ALREADY HAS
-- study_master/
-- site_master/
-- sample_plan/

-- inside container:

-- ctms-landing

-- then automatically you can access:

-- /Volumes/clinical/source/ctms_volume/study_master/

-- /Volumes/clinical/source/ctms_volume/site_master/

-- /Volumes/clinical/source/ctms_volume/sample_plan/

-- WITHOUT creating folders again.


-- IF SUBDIRECTORIES DO NOT EXIST?

-- Then:

-- /Volumes/... paths also won't exist

-- until:

-- folders are created
-- OR
-- files arrive

-- COMMAND ----------

-- VOLUME ≠ COPY

-- External Volume does NOT:

-- move data
-- create data
-- replicate data

-- It only:

-- maps storage into Unity Catalog namespace
