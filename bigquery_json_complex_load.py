from google.cloud import bigquery
from google.cloud import storage
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='D:\Pycharm\GCP\key-bigquery-practice-sample-fb58a943c40b.json'
def upload_gcs_bucket():
    storage_client=storage.Client()
    try:
        bucket=storage_client.get_bucket('gcs-sample-bucket')
        blob=bucket.blob('complex_load.json')
        with open('D:\Pycharm\complex_biquery_adjust.json','rb') as fl:
            blob.upload_from_file(fl)
    except Exception as e:
        print(e)
upload_gcs_bucket()
def upload_json_gcs():
    try:
        Client=bigquery.Client()
        project=Client.project
        datset_ref=bigquery.DatasetReference(project,'gcp_practice_sample')
        schema=[
            bigquery.SchemaField("name","STRING",mode="NULLABLE"),
            bigquery.SchemaField("age", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField(
                "cars",
                "RECORD",
                mode="REPEATED",
                fields=[
                    bigquery.SchemaField("name","STRING",mode="NULLABLE"),
                    bigquery.SchemaField()
        ]

