import os  
import Image
import ImageEnhance 
from django.template import Library  
from django.conf import settings  
  
register = Library()  
  
def thumbnail(original_image_path, size='100x100'):  
    return crop_image_or_return_path(original_image_path, size)
  
register.filter(thumbnail)

def bw_thumbnail(original_image_path, size='100x100'):
    return crop_image_or_return_path(original_image_path, size, greyscale=True)
    
register.filter(bw_thumbnail)

def crop_image_or_return_path(original_image_path, size, greyscale=False):
    if not original_image_path:
        return
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    basename, format = original_image_path.rsplit('.', 1)
    basename, name = basename.rsplit('/', 1)
    miniature = basename + '/thumbnails/' + name + '_' + size
    if (greyscale):
        miniature = miniature + '_bw'
    miniature = miniature + '.' +  format
    
    if not os.path.exists(basename + '/thumbnails/'):
        os.mkdir(basename + '/thumbnails/')
    miniature_filename = os.path.join(settings.MEDIA_ROOT, miniature)
    miniature_url = os.path.join(settings.MEDIA_URL, miniature)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename) \
        or os.path.getmtime(original_image_path) > os.path.getmtime(miniature_filename):
        filename = os.path.join(settings.MEDIA_ROOT, original_image_path)
        image = Image.open(filename)
        image_x, image_y = image.size
        crop_ratio = x / float(y)
        image_ratio = image_x / float(image_y)
        if crop_ratio < image_ratio:
            # x needs to shrink
            top = 0
            bottom = image_y
            crop_width = int(image_y * crop_ratio)
            left = (image_x - crop_width) // 2
            right = left + crop_width
        else:  
            # y needs to shrink
            left = 0
            right = image_x
            crop_height = int(image_x * crop_ratio)
            top = (image_y - crop_height) // 2
            bottom = top + crop_height
        
        image = image.crop((left, top, right, bottom)).resize((x,y), Image.ANTIALIAS)
        
        if (greyscale):
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(0)
            
        image.save(miniature_filename, image.format)
    start, end = miniature_filename.rsplit('/media/', 1)
    return '/media/'+end