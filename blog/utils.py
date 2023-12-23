from django.core.exceptions import ValidationError 
from PIL import Image


def check_image_size(image_path, target_width, target_height):
    ''' validate the size of an image
        image_path: part to image
        target_width: specified width
        target_height: target_height
    '''

    with Image.open(image_path) as img:
        width, height = img.size
        img = img.resize((target_width, target_height))
        img.save(image_path)

