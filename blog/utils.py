from PIL import Image
import os

def check_image_size(image_path, target_width, target_height):
    ''' validate the size of an image
        image_path: part to image
        target_width: specified width
        target_height: target_height
    '''
    if os.path.exists(image_path):
        with Image.open(image_path) as img:
            width, height = img.size
            img = img.resize((target_width, target_height))

            # save and restore the image in its original path
            img.save(image_path)

class ImageSizeValidationMixin:
    def get_queryset(self):
        ''' Validates the size of images in the given queryset
        '''
        queryset = super().get_queryset()

        img_width = 1200
        img_height = 600
        for blog in queryset:
            if blog.image:
                print(blog.image.path)
                check_image_size(blog.image.path, img_width, img_height)
        
        return queryset