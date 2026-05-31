# Databricks notebook source
# MAGIC %md
# MAGIC creating volumes for each source file

# COMMAND ----------

folders = [

    # ================================================
    # CTMS LANDING DATASETS
    # ================================================

    "/Volumes/clinical/source/ctms_volume/study_master/",
    "/Volumes/clinical/source/ctms_volume/site_master/",
    "/Volumes/clinical/source/ctms_volume/visit_schedule/",
    "/Volumes/clinical/source/ctms_volume/sample_plan/",
    "/Volumes/clinical/source/ctms_volume/test_plan/",
    "/Volumes/clinical/source/ctms_volume/protocol_version/",
    "/Volumes/clinical/source/ctms_volume/treatment_arm/",
    "/Volumes/clinical/source/ctms_volume/visit_activity_plan/",
    "/Volumes/clinical/source/ctms_volume/study_site_map/",
    "/Volumes/clinical/source/ctms_volume/study_enrollment_plan/",
    "/Volumes/clinical/source/ctms_volume/investigator_master/",
    "/Volumes/clinical/source/ctms_volume/consent_master/",
    "/Volumes/clinical/source/ctms_volume/sample_type_master_ctms/",

    # ================================================
    # AUTLOADER INTERNAL FOLDERS
    # ================================================

    "/Volumes/clinical/source/ctms_volume/_schema/",
    "/Volumes/clinical/source/ctms_volume/_checkpoints/",
    "/Volumes/clinical/source/ctms_volume/_temp/"
]

for folder in folders:

    dbutils.fs.mkdirs(folder)

    print(f"Created: {folder}")

# COMMAND ----------

# These:

# study_master/
# site_master/
# sample_plan/

# are OPTIONAL to pre-create.

# Because:

# files arriving will create them automatically

# COMMAND ----------

# These are MUCH more commonly pre-created:

# _schema/
# _checkpoints/
# _temp/

# because:

# system-controlled
# framework-owned
# important for streaming stability

# VERY common to create manually.

# COMMAND ----------

display(
    dbutils.fs.ls(
        "/Volumes/clinical/source/ctms_volume/"
    )
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES IN clinical.source;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE VOLUME clinical.source.ctms_volume;

# COMMAND ----------

# VERY IMPORTANT

# Once you create:

# CREATE EXTERNAL VOLUME clinical.source.ctms_volume
# LOCATION 'abfss://ctms-landing@pfizerclinicaldata.dfs.core.windows.net/';

# the ENTIRE container becomes exposed through:

# /Volumes/clinical/source/ctms_volume/
# NOW WHAT HAPPENS?

# Suppose ADF later writes:

# abfss://ctms-landing@pfizerclinicaldata.dfs.core.windows.net/study_master/file1.csv

# Immediately:

# /Volumes/clinical/source/ctms_volume/study_master/file1.csv

# becomes visible automatically.

# WITHOUT:

# creating another volume
# creating another mapping
# creating folder manually

# VERY important.

# SO VOLUME IS LIKE A LIVE WINDOW

# Think of external volume as:

# live filesystem bridge

# between:

# ADLS
# Unity Catalog

# COMMAND ----------

# EXAMPLE
# ADLS CONTAINER
# ctms-landing/
# │
# ├── study_master/
# ├── site_master/
# ├── protocol_version/
# ├── shipment/
# ├── lims/
# SINGLE EXTERNAL VOLUME
# CREATE EXTERNAL VOLUME clinical.source.ctms_volume
# LOCATION 'abfss://ctms-landing@pfizerclinicaldata.dfs.core.windows.net/';
# AUTOMATICALLY EXPOSES
# /Volumes/clinical/source/ctms_volume/study_master/

# /Volumes/clinical/source/ctms_volume/site_master/

# /Volumes/clinical/source/ctms_volume/protocol_version/

# /Volumes/clinical/source/ctms_volume/shipment/

# /Volumes/clinical/source/ctms_volume/lims/

# ALL automatically.

# NO NEED TO CREATE

# ❌ volume per folder
# ❌ volume per table
# ❌ manual folder registration
# ❌ manual UC sync

# VERY important.

# COMMAND ----------

# IMPORTANT LIMIT

# Permissions are still primarily:

# volume-level

# NOT:

# folder-level usually

# That is why:

# volume-per-security-domain

# is the sweet spot.

# FINAL ANSWER

# YES — once external volume is created:

# /Volumes/clinical/source/ctms_volume/

# ANY new folders/files created in ADLS automatically appear inside the volume path.

# ADF/vendors creating:

# study_master/
# site_master/
# sample_plan/

# automatically makes them accessible via:

# /Volumes/clinical/source/ctms_volume/...

# No new volume creation is needed.
