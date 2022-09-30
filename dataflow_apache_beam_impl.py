import apache_beam as beam
from apache_beam.io.gcp.internal.clients import bigquery
from apache_beam.options.pipeline_options import PipelineOptions
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='D:\Pycharm\GCP\key-bigquery-practice-sample-fb58a943c40b.json'

import argparse

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--experiment',
    default='use_unsupported_python_version',
    help='This does not seem to do anything.')
  args, beam_args = parser.parse_known_args()
  return beam_args

def beamer(rows=[]):
  if len(rows) == 0:
    return

  project = 'bigquery-practice-sample'
  gcs_temp_location = 'gs://gcs-sample-bucket/dataflow-error-bucket'
  gcs_staging_location = 'gs://gcs-sample-bucket/'

  table_spec = bigquery.TableReference(
    projectId=project,
    datasetId='gcp_practice_sample',
    tableId='emp_sample_details_dataflow')
  beam_options = PipelineOptions(
    parseArgs(), # This doesn't seem to work.
    project=project,
    runner='DataflowRunner',
    job_name='sample-run-pipeline',
    temp_location=gcs_temp_location,
    staging_location=gcs_staging_location,
    region='us-east1',
    use_unsupported_python_version=True, # This doesn't work either. :(
    experiments=['use_unsupported_python_version'] # This also doesn't work.
  )

  with beam.Pipeline(options=beam_options) as p:
    quotes = p | beam.Create(rows)

    quotes | beam.io.WriteToBigQuery(
    table_spec,
    # custom_gcs_temp_location = gcs_temp_location, # Not needed?
    method='FILE_LOADS',
    schema={
      "fields":[{"name":"Name","type":"STRING","mode":"REQUIRED"},
                      {"name":"EmpId","type":"INTEGER","mode":"REQUIRED"},
                      {"name": "Salary", "type":"INTEGER","mode": "REQUIRED"},
                      {"name": "Dept", "type":"String","mode": "REQUIRED"},
                      {"name": "DeptId", "type":"INTEGER", "mode": "REQUIRED"},
                      {"name": "Designation", "type":"String", "mode": "REQUIRED"},
                                            ]},
    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
  return

if __name__ == '__main__':
    beamer(rows=[{'Name': 'Mohan','EmpId':345,'Salary':657,'Dept':'Finance','DeptId':11,'Designation':'Accountant'}])
