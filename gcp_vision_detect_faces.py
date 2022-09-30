import os,io,re
from google.cloud import vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="D:\Pycharm\ServiceAccount_VisionAPI.json"
client=vision.ImageAnnotatorClient()

file_path='D:\Pycharm\emotions.jpg'
with io.open(file_path,'rb') as file_open:
    content=file_open.read()
image=vision.types.Image(content=content)
response=client.face_detection(image)
faceAnnotations=response.face_annotations
print('Faces :')
likehood=('Unknown','Very Unlikely','Unlikely','Possibly','Likely','Very Likely')
for face in faceAnnotations:
    print('Detection confidence {0}'.format(face.detection_confidence))
    print('Angry likelyhood : {0}'.format(likehood[face.anger_likelihood]))
    print('Joy likelyhood: {0}'.format(likehood[face.joy_likelihood]))
    print('Sorrow likelyhood: {0}'.format(likehood[face.sorrow_likelihood]))
    print('Surprise likelyhood: {0} '.format(likehood[face.surprise_likelihood]))
    print('Headwear likelyhood: {0}'.format(likehood[face.headwear_likelihood]))
