import os,io,re
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import storage
from google.protobuf import json_format
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="D:\Pycharm\ServiceAccount_VisionAPI.json"
client=vision.ImageAnnotatorClient()
batch_size=2
mime_type='application/pdf'
feature=vision.types.Feature(
    type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)
gcs_source_uri="gs://data_analytics_bucket_storage/ICICI_Statement.pdf"
gcs_source=vision.types.GcsSource(uri=gcs_source_uri)
input_config=vision.types.InputConfig(gcs_source=gcs_source,mime_type=mime_type)
gcs_destination_uri='gs://data_analytics_bucket_storage/pdf_result'
gcs_destination=vision.types.GcsDestination(uri=gcs_destination_uri)
output_config=vision.types.OutputConfig(gcs_destination=gcs_destination,batch_size=batch_size)
async_request=vision.types.AsyncAnnotateFileRequest(
    features=[feature],input_config=input_config,output_config=output_config
)
operation=client.async_batch_annotate_files(requests=[async_request])
operation.result(timeout=120)
storage_client=storage.Client()
match=re.match('gs://([^/]+)/(.+)',gcs_destination_uri)
bucket_name=match.group(1)
prefix=match.group(2)
bucket=storage_client.get_bucket(bucket_name)
blob_list=list(bucket.list_blobs(prefix=prefix))
print('Output files :')
for blob in blob_list:
    print(blob.name)
output=blob_list[0]
json_string=output.download_as_string()
response=json_format.Parse(
    json_string,vision.types.AnnotateFileResponse()
)
first_page_response=response.responses[0]
annotation=first_page_response.full_text_annotation
print('Full Text :')
print(annotation.text)
