import  os,io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="D:\Pycharm\ServiceAccount_VisionAPI.json"
client=vision.ImageAnnotatorClient()
FOLDER_PATH='D:\Pycharm'
IMAGE_FILE='March_Salary_2022.png'
FILE_PATH=os.path.join(FOLDER_PATH,IMAGE_FILE)
with io.open(FILE_PATH,'rb') as image_file:
    content=image_file.read()
image=vision.types.Image(content=content)
response=client.document_text_detection(image=image)
doctext=response.full_text_annotation.text
print(doctext)

pages=response.full_text_annotation.pages
for page in pages:
    for block in page.blocks:
        print('block confidence : ',block.confidence)
        for paragraph in block.paragraphs:
            print('paragraph confidence :',paragraph.confidence)
            for word in paragraph.words:
                word_text=''.join([symbol.text for symbol in word.symbols])
                print('Word text : {0} (confidence : {1}'.format(word_text,word.confidence))
                for symbol in word.symbols:
                    print('\t Symbol : {0} (confidence : {1}'.format(symbol.text,symbol.confidence))