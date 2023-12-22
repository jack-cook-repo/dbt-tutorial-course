import pandas as pd
from google.cloud import bigquery
import pandas_gbq

# Set your project ID
project_id = "numeric-abbey-406522"

# Set the BigQuery dataset and table names
dataset_id = "dbtbigquery"
table_id = "mt_cars"

# Set the path to your Parquet file
parquet_file_path = "/home/xinyu/dbt-tutorial-course/data/mt_cars.parquet"

# Load Parquet file into a pandas DataFrame
df = pd.read_parquet(parquet_file_path)

# Initialize a BigQuery client
client = bigquery.Client(project=project_id)

# Specify the destination table in BigQuery
destination_table = f"{project_id}.{dataset_id}.{table_id}"

# Write the DataFrame to BigQuery
pandas_gbq.to_gbq(df, destination_table, project_id=project_id, if_exists='replace')
