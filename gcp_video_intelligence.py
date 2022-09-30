import os
from google.cloud import videointelligence
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="D:\Pycharm\ServiceAccount_VisionAPI.json"
video_client=videointelligence.VideoIntelligenceServiceClient()
features=[videointelligence.enums.Feature.LABEL_DETECTION]
gs_file="gs://video_search_intelligence/file_example_MP4_1920_18MG.mp4"
operation=video_client.annotate_video(gs_file,features=features)
result=operation.result(timeout=120)
annotation_result=result.annotation_results[0]
for segment_label in annotation_result.segment_label_annotations:
    print('Video Label description : {0}'.format(segment_label.entity.description))
    print(segment_label)
