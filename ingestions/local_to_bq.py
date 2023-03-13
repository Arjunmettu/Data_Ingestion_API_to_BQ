import os
import requests
import pandas as pd
import json

from google.cloud import bigquery





# Set up BigQuery client
client = bigquery.Client()

# Set up variables for folder and dataset/table names
folder_path = '/Users/Arjun/Documents/Datasets/all_json'
dataset_name = 'my_dataset'
table_prefix = 'json_'

# Get list of JSON files in folder
file_list = [os.path.join(folder_path, f) 
for f in os.listdir(folder_path) if f.endswith('.json')]

# Loop through each file and create/load table in BigQuery
for file_path in file_list:
    # Extract table name from file name
    table_name = table_prefix + os.path.splitext(os.path.basename(file_path))[0]

    # Create table schema based on JSON file
    with open(file_path) as f:
        first_line = f.readline().strip()
    schema = bigquery.SchemaField('data', 'RECORD', mode='REQUIRED', fields=bigquery.SchemaField.from_api_repr(json.loads(first_line)).values())

    # Create or get dataset
    dataset_ref = client.dataset(dataset_name)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = 'US'
    dataset = client.create_dataset(dataset, exists_ok=True)

    # Create or get table and load data from file
    table_ref = dataset.table(table_name)
    job_config = bigquery.LoadJobConfig(schema=[schema], source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON)
    with open(file_path, 'rb') as f:
        job = client.load_table_from_file(f, table_ref, job_config=job_config)
    job.result()  # Wait for job to complete

    print(f'Loaded {table_name} from {file_path} into BigQuery')