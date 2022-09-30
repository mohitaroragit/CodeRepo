from google.cloud import bigquery
import os
client=bigquery.Client()
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='D:\Pycharm\GCP\gkey-bigquery-practice-sample-31e14021aadb.json'
rows_table=client.list_rows('bigquery-practice-sample.practice_data_manipulation.json_load_tbl')
rows=list(rows_table)
print("the Downloaded {} rows from the table {} ".format(rows,rows_table))
table_id='bigquery-practice-sample.gcp_practice_sample.load_tbl_from_code'
job_config=bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("name","STRING"),
        bigquery.SchemaField("post_abbr","STRING"),
],
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
)
uri="gs://cloud-samples-data/bigquery/us-states/us-states.json"
load_job=client.load_table_from_uri(
    uri,
    table_id,
    location="US",
    job_config=job_config,
)
load_job.result()
destination_table=client.get_table(table_id)
print("Landed {} rows".format(destination_table.num_rows))