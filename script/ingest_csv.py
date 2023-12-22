import pandas as pd
import boto3
import argparse
from botocore.exceptions import NoCredentialsError
from datetime import datetime
from google.cloud import bigquery

BUCKET = 'test-instance1'
PROJECT_ID = "numeric-abbey-406522"


# Set your Google Cloud credentials (replace 'your-project-id' with your actual project ID)
# You can obtain the credentials JSON file from the Google Cloud Console.
# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of the JSON file.

# Example:
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"



def read_file_from_s3(file_name):

    s3 = boto3.client('s3')
    file_name = "dbt-bigquery/landing/"+file_name
    obj = s3.get_object(Bucket= BUCKET, Key= file_name)

    df = pd.read_csv(obj['Body']) 
    return df


def main(args):
    table_id = args.table_id
    database_id = args.database_id
    file_name = args.file_name

    #Reading csv file from S3 bucker
    df = read_file_from_s3(file_name)
    #Add day partition
    df['day']= datetime.today().strftime('%Y-%m-%d')
    # Save the DataFrame to BigQuery
    df.to_gbq(destination_table=f"{PROJECT_ID}.{database_id}.{table_id}", project_id=PROJECT_ID, if_exists="replace")



if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--file_name", help="The filename you want to ingest")
    argParser.add_argument("-d", "--database_id", help="The database you want to ingest in big query", default="dbtbigquery")
    argParser.add_argument('-t', "--table_id", help="The table name you want in big query")
    args = argParser.parse_args()
    main(args)
