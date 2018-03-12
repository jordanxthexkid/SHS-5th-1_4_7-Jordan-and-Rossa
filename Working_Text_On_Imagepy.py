# -*- coding: utf-8 -*-
import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageEnhance
import os, sys

#the code below just replaces the picture with text and doesn't create a mask
#img = Image.new('RGB', (100, 30), color = (73, 109, 137))
#d = ImageDraw.Draw(img)
#d.text((10,10), "Hello World", fill=(255,255,0))
#img.save('basketball.png') 

FONT = 'Arial.ttf'
 
def add_watermark(in_file, text, out_file='GlassCoke.jpg', angle=0, opacity=0.75):
    img = Image.open('GlassCoke.png').convert('RGB')
    watermark = Image.new('RGBA', img.size, (0,0,0,0))
    size = 10
    n_font = ImageFont.truetype(FONT, size)
    n_width, n_height = n_font.getsize(text)
    while n_width+n_height < watermark.size[0]:
        size += 2
        n_font = ImageFont.truetype(FONT, size)
        n_width, n_height = n_font.getsize(text)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - n_width) / 2,
              (watermark.size[1] - n_height) / 12),
              text, font=n_font)
    watermark = watermark.rotate(angle,Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    Image.composite(watermark, img, watermark).save(out_file, 'JPEG')
if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('Usage: %s <input-image> <text> <output-image> ' \
                 '<angle> <opacity> ' % os.path.basename(sys.argv[0]))
    add_watermark(*sys.argv[1:]) 

def frame(original_image,color,frame_width):
    """ frames the image with a specified color of a PIL.Image
    original_image must be a PIL.Image
    Returns a new PIL.Image with rounded corners, where
    0 < percent_of_side < 1
    is the corner radius as a portion of the shorter dimension of original_image
    """
    #set the radius of the rounded corners
    width, height = original_image.size
    thickness = int(frame_width * min(width, height)) # thickness in pixels
    
    ###
    #create a mask
    ###
    
    #start with transparent mask
    r,g,b=color
    frame_mask = PIL.Image.new('RGBA', (width, height), (0,0,0,0))
    drawing_layer = PIL.ImageDraw.Draw(frame_mask)
    
    # Overwrite the RGBA values with A=255.
    # The 127 for RGB values was used merely for visualizing the mask
    # Draw two rectangles to fill interior with opaqueness
    #drawing_layer.rectangle((0,0,width,thickness),fill=(r,g,b,255))
    #drawing_layer.rectangle((0,height-thickness,width,height),fill=(r,g,b,255))
    #drawing_layer.rectangle((0,height,thickness,0),fill=(r,g,b,255))
    #drawing_layer.rectangle((width,0,width-thickness,height),fill=(r,g,b,255))
    drawing_layer.rectangle((thickness,thickness,width-thickness,height-thickness),fill=(r,g,b,255))
    
    # Make the new image, starting with all transparent
    #frame_image = PIL.Image.new('RGBA',(width,height),(r,g,b,255))
    result = PIL.Image.new('RGBA', original_image.size, (255,0,0,255))#<-- this code hard codes the program to produce a red border
    result.paste(original_image, (0,0), mask=frame_mask)
    return result
    
def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def frame_all_images(color=(255,0,0), directory=None, frame_width= 0.05):
    """ Saves a modfied version of each image in directory.
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and have transparent rounded corners.
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'modified')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    #load all the images
    image_list, file_list = get_images(directory)  

    #go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        filename, filetype = file_list[n].split('.')
        print n
        # Round the corners with radius = 30% of short side
        new_image = frame(image_list[n], color, frame_width)
        #save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)
        