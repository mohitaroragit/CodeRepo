from google.cloud import bigquery
from google.cloud import storage
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='D:\Pycharm\GCP\key-bigquery-practice-sample-fb58a943c40b.json'
def gcs_upload_blob():
    storage_client=storage.Client()
    try:
        bucket=storage_client.get_bucket('gcs-sample-bucket')
        blob=bucket.blob('demo.csv')
        #filepath=r'D:\Pycharm'
        with open('D:\Pycharm\demo.txt','rb') as f:
              blob.upload_from_file(f)
    except Exception as e:
        print(e)

gcs_upload_blob()

def bq_upload_csv_in_gcs():
    try:
        bigquery_client=bigquery.Client()
        dataset_ref=bigquery_client.dataset('gcp_practice_sample')
        table_ref=dataset_ref.table('json-sample-table')
        table=bigquery_client.get_table(table_ref)
        job_config=bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField('id','STRING',mode='REQUIRED'),
            bigquery.SchemaField('type','STRING',mode='REQUIRED'),
            bigquery.SchemaField('name', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('ppu', 'DECIMAL', mode='REQUIRED'),
            bigquery.SchemaField(
                
            )
            ],
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        )
        uri="gs://gcs-sample-bucket/sample.json"
    #job_config.schema=schema
    #job_config.skip_leading_rows=1
        load_job=bigquery_client.load_table_from_uri(uri,table,job_config=job_config,)
    #assert  load_job.job_type=='load'
        load_job.result()
    #assert load_job=='DONE'
    except Exception as e:
        for e in load_job.errors:
            print('Error: {}'.format(e['message']))
#bq_upload_csv_in_gcs()