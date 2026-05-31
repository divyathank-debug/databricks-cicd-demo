-- Databricks notebook source
DROP TABLE IF EXISTS clinical.metadata.schemas;

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS clinical.metadata.schemas
(
    table_name STRING,
    schema_version INT,
    schema_json STRING,
    active_flag BOOLEAN,
    created_at TIMESTAMP
)
USING DELTA;

-- COMMAND ----------

INSERT INTO clinical.metadata.schemas
VALUES
(
'study_master',

1,

'[
 {"name":"study_id","type":"string"},
 {"name":"study_name","type":"string"},
 {"name":"phase","type":"string"},
 {"name":"therapeutic_area","type":"string"},
 {"name":"start_date","type":"date"},
 {"name":"end_date","type":"date"},
 {"name":"status","type":"string"},
 {"name":"region","type":"string"},
 {"name":"protocol_version","type":"string"}
]',

TRUE,

current_timestamp()
);

-- COMMAND ----------

SELECT * FROM clinical.metadata.schemas;

-- COMMAND ----------

-- =====================================================
-- SITE MASTER
-- =====================================================

INSERT INTO clinical.metadata.schemas
VALUES
(
'site_master',

1,

'[
 {"name":"site_id","type":"string"},
 {"name":"site_name","type":"string"},
 {"name":"country","type":"string"},
 {"name":"city","type":"string"},
 {"name":"region","type":"string"},
 {"name":"site_status","type":"string"},
 {"name":"principal_investigator","type":"string"}
]',

TRUE,

current_timestamp()
);

-- =====================================================
-- VISIT SCHEDULE
-- =====================================================

INSERT INTO clinical.metadata.schemas
VALUES
(
'visit_schedule',

1,

'[
 {"name":"visit_id","type":"string"},
 {"name":"study_id","type":"string"},
 {"name":"visit_name","type":"string"},
 {"name":"visit_day","type":"integer"},
 {"name":"window_start_day","type":"integer"},
 {"name":"window_end_day","type":"integer"}
]',

TRUE,

current_timestamp()
);

-- =====================================================
-- SAMPLE PLAN
-- =====================================================

INSERT INTO clinical.metadata.schemas
VALUES
(
'sample_plan',

1,

'[
 {"name":"sample_plan_id","type":"string"},
 {"name":"study_id","type":"string"},
 {"name":"visit_id","type":"string"},
 {"name":"sample_type","type":"string"},
 {"name":"planned_quantity","type":"integer"},
 {"name":"collection_timepoint","type":"string"}
]',

TRUE,

current_timestamp()
);

-- =====================================================
-- TEST PLAN
-- =====================================================

INSERT INTO clinical.metadata.schemas
VALUES
(
'test_plan',

1,

'[
 {"name":"test_plan_id","type":"string"},
 {"name":"study_id","type":"string"},
 {"name":"sample_type","type":"string"},
 {"name":"test_name","type":"string"},
 {"name":"lab_vendor","type":"string"},
 {"name":"priority","type":"string"}
]',

TRUE,

current_timestamp()
);

-- =====================================================
-- PROTOCOL VERSION
-- =====================================================

INSERT INTO clinical.metadata.schemas
VALUES
(
'protocol_version',

1,

'[
 {"name":"protocol_version_id","type":"string"},
 {"name":"study_id","type":"string"},
 {"name":"protocol_version","type":"string"},
 {"name":"effective_date","type":"date"},
 {"name":"approval_status","type":"string"}
]',

TRUE,

current_timestamp()
);

-- =====================================================
-- TREATMENT ARM
-- =====================================================

INSERT INTO clinical.metadata.schemas
VALUES
(
'treatment_arm',

1,

'[
 {"name":"treatment_arm_id","type":"string"},
 {"name":"study_id","type":"string"},
 {"name":"arm_name","type":"string"},
 {"name":"arm_type","type":"string"},
 {"name":"dosage","type":"string"}
]',

TRUE,

current_timestamp()
);

-- =====================================================
-- VISIT ACTIVITY PLAN
-- =====================================================

INSERT INTO clinical.metadata.schemas
VALUES
(
'visit_activity_plan',

1,

'[
 {"name":"activity_id","type":"string"},
 {"name":"visit_id","type":"string"},
 {"name":"activity_name","type":"string"},
 {"name":"activity_type","type":"string"},
 {"name":"mandatory_flag","type":"string"}
]',

TRUE,

current_timestamp()
);

-- =====================================================
-- STUDY SITE MAP
-- =====================================================

INSERT INTO clinical.metadata.schemas
VALUES
(
'study_site_map',

1,

'[
 {"name":"study_site_map_id","type":"string"},
 {"name":"study_id","type":"string"},
 {"name":"site_id","type":"string"},
 {"name":"site_activation_date","type":"date"},
 {"name":"site_status","type":"string"}
]',

TRUE,

current_timestamp()
);

-- =====================================================
-- STUDY ENROLLMENT PLAN
-- =====================================================

INSERT INTO clinical.metadata.schemas
VALUES
(
'study_enrollment_plan',

1,

'[
 {"name":"enrollment_plan_id","type":"string"},
 {"name":"study_id","type":"string"},
 {"name":"site_id","type":"string"},
 {"name":"planned_subject_count","type":"integer"},
 {"name":"planned_enrollment_date","type":"date"}
]',

TRUE,

current_timestamp()
);

-- =====================================================
-- INVESTIGATOR MASTER
-- =====================================================

INSERT INTO clinical.metadata.schemas
VALUES
(
'investigator_master',

1,

'[
 {"name":"investigator_id","type":"string"},
 {"name":"investigator_name","type":"string"},
 {"name":"specialization","type":"string"},
 {"name":"country","type":"string"},
 {"name":"email","type":"string"}
]',

TRUE,

current_timestamp()
);

-- =====================================================
-- CONSENT MASTER
-- =====================================================

INSERT INTO clinical.metadata.schemas
VALUES
(
'consent_master',

1,

'[
 {"name":"consent_id","type":"string"},
 {"name":"study_id","type":"string"},
 {"name":"consent_version","type":"string"},
 {"name":"effective_date","type":"date"},
 {"name":"consent_status","type":"string"}
]',

TRUE,

current_timestamp()
);

-- =====================================================
-- SAMPLE TYPE MASTER CTMS
-- =====================================================

INSERT INTO clinical.metadata.schemas
VALUES
(
'sample_type_master_ctms',

1,

'[
 {"name":"sample_type_id","type":"string"},
 {"name":"sample_type_name","type":"string"},
 {"name":"container_type","type":"string"},
 {"name":"storage_temperature","type":"string"},
 {"name":"processing_requirement","type":"string"}
]',

TRUE,

current_timestamp()
);
