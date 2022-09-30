import os,io
from google.cloud import vision
import pandas as pd
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="D:\Pycharm\ServiceAccount_VisionAPI.json"
client=vision.ImageAnnotatorClient()
image_path='D:\Pycharm\Statue_Of_Liberty.jpg'
with io.open(image_path,'rb') as image_file:
    content=image_file.read()
image=vision.types.Image(content=content)
response=client.landmark_detection(image=image)
landmarks=response.landmark_annotations
df=pd.DataFrame(columns=['description','locations','score'])
for landmark in landmarks:
    df=df.append(
        dict(
            description=landmark.description,
            location=landmark.locations,
            score=landmark.score

        ),ignore_index=True
    )
print(df)

# print(landmarks)