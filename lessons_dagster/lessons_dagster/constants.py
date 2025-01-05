from pathlib import Path
import os

START_DATE = "2024-01-01"
END_DATE = "2025-04-01"

os.environ['DBT_PROFILES_DIR'] = "."
os.environ['BIGQUERY_PROJECT'] = "dbt-test-445518"
