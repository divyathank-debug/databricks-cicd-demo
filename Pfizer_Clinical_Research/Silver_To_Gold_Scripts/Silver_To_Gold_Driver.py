# Databricks notebook source
# =====================================================
# GOLD DRIVER NOTEBOOK
# Clinical Research Gold Layer Orchestration
# =====================================================

import time
from datetime import datetime
# dbutils.widgets.text("run_id", "")
# dbutils.widgets.text("table_metadata", "")

# run_id = dbutils.widgets.get("run_id")
# table_metadata = dbutils.widgets.get("table_metadata")

# =====================================================
# GOLD NOTEBOOK CONFIGURATION
# =====================================================

gold_notebooks = [

    {
        "table_name": "sample_tracking_summary",
        "notebook_path":
        "/Workspace/Users/divya.thank@gmail.com/Pfizer_Clinical_Research/Silver_To_Gold_Scripts/gold_transformations/sample_tracking_summary"
    },

    {
        "table_name": "lab_performance",
        "notebook_path":
        "/Workspace/Users/divya.thank@gmail.com/Pfizer_Clinical_Research/Silver_To_Gold_Scripts/gold_transformations/lab_performance"
    },

    {
        "table_name": "shipment_sla_summary",
        "notebook_path":
        "/Workspace/Users/divya.thank@gmail.com/Pfizer_Clinical_Research/Silver_To_Gold_Scripts/gold_transformations/shipment_sla_summary"
    },

    {
        "table_name": "study_enrollment_summary",
        "notebook_path":
        "/Workspace/Users/divya.thank@gmail.com/Pfizer_Clinical_Research/Silver_To_Gold_Scripts/gold_transformations/study_enrollment_summary"
    },

    {
        "table_name": "freezer_utilization_summary",
        "notebook_path":
        "/Workspace/Users/divya.thank@gmail.com/Pfizer_Clinical_Research/Silver_To_Gold_Scripts/gold_transformations/freezer_utilization_summary"
    }
]

# =====================================================
# EXECUTION LOOP
# =====================================================

pipeline_start_time = datetime.now()

print("==========================================")
print("STARTING GOLD LAYER EXECUTION")
print(f"Start Time : {pipeline_start_time}")
print("==========================================")

success_count = 0
failure_count = 0

for notebook in gold_notebooks:

    table_name = notebook["table_name"]
    notebook_path = notebook["notebook_path"]

    print("\n==========================================")
    print(f"STARTING : {table_name}")
    print(f"Notebook : {notebook_path}")
    print("==========================================")

    start_time = time.time()

    try:

        # ============================================
        # RUN NOTEBOOK
        # ============================================

        row_count = dbutils.notebook.run(
            notebook_path,
            timeout_seconds=3600
        )

        end_time = time.time()

        duration_seconds = round(
            end_time - start_time,
            2
        )

        success_count += 1

        print("==========================================")
        print(f"SUCCESS : {table_name}")
        print(f"Rows    : {row_count}")
        print(f"Duration: {duration_seconds} seconds")
        print("==========================================")

    except Exception as e:

        failure_count += 1

        end_time = time.time()

        duration_seconds = round(
            end_time - start_time,
            2
        )

        print("==========================================")
        print(f"FAILED : {table_name}")
        print(f"Duration : {duration_seconds} seconds")
        print(f"Error : {str(e)}")
        print("==========================================")

        raise

# =====================================================
# PIPELINE SUMMARY
# =====================================================

pipeline_end_time = datetime.now()

print("\n==========================================")
print("GOLD PIPELINE COMPLETED")
print(f"Start Time    : {pipeline_start_time}")
print(f"End Time      : {pipeline_end_time}")
print(f"Success Count : {success_count}")
print(f"Failure Count : {failure_count}")
print("==========================================")
