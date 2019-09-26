from google.cloud import vision
from google.cloud.vision import types
import io
import os
from PIL import Image, ImageDraw
from enum import Enum

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\Joel Monteiro\\Desktop\\Product Demo 3.0\\GCP Vision.json"

image_file='Wachovia.jpg'
image  = Image.open(image_file)
client = vision.ImageAnnotatorClient()
with io.open(image_file, 'rb') as image_file1:
        content = image_file1.read()
content_image = types.Image(content=content)
response = client.document_text_detection(image=content_image)
document = response.full_text_annotation

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def draw_boxes(image, bounds, color, width=3):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y,
            bound.vertices[0].x, bound.vertices[0].y], fill=color, width=width)
        image.save("tmp.png")
        tmp = Image.open('tmp.png')
        tmp.show
    return image


def get_document_bounds(response, feature):
    bounds = []
    for i, page in enumerate(document.pages):
        for block in page.blocks:
            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)
            for paragraph in block.paragraphs:
                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)
                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)
    return bounds
#change WORD/PARA
bounds = get_document_bounds(response, FeatureType.WORD)
draw_boxes(image, bounds, 'white')

print("fin")