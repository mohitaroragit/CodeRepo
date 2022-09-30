import os,re,io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="D:\Pycharm\ServiceAccount_VisionAPI.json"
client=vision.ImageAnnotatorClient()
file_path='D:\Pycharm\Building_house.jpg'
aspect_ratios=[4/3]
def cropHint(file_path,aspect_ratios):
    with io.open(file_path,'rb') as img_file:
        content=img_file.read()
    image=vision.types.Image(content=content)
    crop_hint_params=vision.types.CropHintsParams(aspect_ratios=aspect_ratios)
    image_context=vision.types.ImageContext(
        crop_hints_params=crop_hint_params
    )
    response=client.crop_hints(
        image=image,
        image_context=image_context
    )
    cropHints=response.crop_hints_annotation.crop_hints
    for crophint in cropHints:
        print('Confidence : ',crophint.confidence)
        print('Importance Fraction :',crophint.importance_fraction)
        print('Vertices',crophint.bounding_poly)
cropHint(file_path,aspect_ratios)