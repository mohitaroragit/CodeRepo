import os,re,io
from google.cloud import vision
import pandas as pd
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="D:\Pycharm\ServiceAccount_VisionAPI.json"
client=vision.ImageAnnotatorClient()
image_path='D:\Pycharm\cat_image.jpg'
with io.open(image_path,'rb') as image_file:
    content=image_file.read()
image=vision.types.Image(content=content)
response=client.label_detection(image=image)
labels=response.label_annotations
df=pd.DataFrame(columns=['description','score','topicality'])
for label in labels:
    df=df.append(
        dict(
            description=label.description,
            score=label.score,
            topicality=label.topicality

        ),ignore_index=True
    )
print(df)