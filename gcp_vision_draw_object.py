import os,io
from google.cloud import vision
from draw_vertices import drawVertices
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="D:\Pycharm\ServiceAccount_VisionAPI.json"
client=vision.ImageAnnotatorClient()
image_file="D:\Pycharm\office_microsoft_image.jpg"
with io.open(image_file,'rb') as image_file_open:
    content=image_file_open.read()
image=vision.types.Image(content=content)
response=client.logo_detection(image=image)
logos=response.logo_annotations
for logo in logos:
    print('Logo Description :',logo.description)
    print('Confidence score {0}'.format(logo.score))
    print('-' *50)
    vertices=logo.bounding_poly.vertices
    print('Vertices Value {0}'.format(vertices))
    drawVertices(content,vertices,logo.description)