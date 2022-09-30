import os,io
from google.cloud import  vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="D:\Pycharm\ServiceAccount_VisionAPI.json"
client=vision.ImageAnnotatorClient()
file_image='D:\Pycharm\Building_house.jpg'
with io.open(file_image,'rb') as file_cature:
    content=file_cature.read()
image=vision.types.Image(content=content)
response=client.label_detection(image=image)
print(response)