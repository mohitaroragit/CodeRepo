import os,io
from google.cloud import vision
from numpy import random
from Pillow_Utility import draw_borders,Image
import pandas as pd
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="D:\Pycharm\ServiceAccount_VisionAPI.json"
client=vision.ImageAnnotatorClient()
image_file="D:\Pycharm\ikea_image_1.jpg"
with io.open(image_file,'rb') as image_path:
    content=image_path.read()
image=vision.types.Image(content=content)
response=client.object_localization(image=image)
localized_object_annotations=response.localized_object_annotations
df=pd.DataFrame(columns=['name','score'])
for obj in localized_object_annotations:
    df=df.append(
        dict(
            name=obj.name,
            score=obj.score
        ),
        ignore_index=True
    )
#print(df)
pillow_image=Image.open(image_file)
for obj in localized_object_annotations:
    #r,g,b=random.randint(150,255),random.randint(150,255),random.randint(150,255)
    r,g,b=255,255,255
    draw_borders(pillow_image,obj.bounding_poly,(r,g,b),
                 pillow_image.size,obj.name,obj.score)
pillow_image.show()