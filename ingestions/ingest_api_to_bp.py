import os
import csv
import json
import requests
from google.cloud import bigquery
from google.oauth2 import service_account

# Set up Google Cloud credentials
key_path = '/Users/Arjun/Downloads/Videographers/key.json'
credentials = service_account.Credentials.from_service_account_file(key_path)
project_id = 'your-project-id'
dataset_id = 'your-dataset-id'
table_id = 'your-table-id'

# Define API endpoint and parameters
url = 'https://api.covid19india.org/state_district_wise.json'
params = {'param1': 'value1', 'param2': 'value2'}

# Send GET request to API and retrieve JSON response
response = requests.get(url, params=params)
data = json.loads(response.text)

# Load data into BigQuery
client = bigquery.Client(project=project_id, credentials=credentials)
table_ref = client.dataset(dataset_id).table(table_id)
table = client.get_table(table_ref)

rows_to_insert = []
for item in data:
    rows_to_insert.append((item['column1'], item['column2'], item['column3']))

errors = client.insert_rows(table, rows_to_insert)
if errors:
    print(f'Encountered errors while inserting rows: {errors}')
else:
    print('Data successfully loaded into BigQuery.')

# Export data to CSV file
filename = 'data.csv'
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['column1', 'column2', 'column3'])
    for item in data:
        writer.writerow([item['column1'], item['column2'], item['column3']])
print(f'Data successfully exported to {filename}.')

# Push code to Git repository
repo_path = 'https://github.com/Arjunmettu/Data_Ingestion_API_to_BQ.git'
os.chdir(repo_path)
os.system('git add .')
os.system('git commit -m "Added code to ingest data from API and load into BigQuery."')
os.system('git push origin main')
print('Code successfully pushed to Git repository.')