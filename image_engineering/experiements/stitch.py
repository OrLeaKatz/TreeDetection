import os
from PIL import Image
import numpy as np
import re

original_img_xy_re = ".*_(\d+)_(\d+)"
tiles_xy_re = ".*__(\d+)_(\d+)__"
        

def stitch(dir_path, save_path , pixel_size,  in_canels=1, choice=0):
    """
    function stitches together tiles to repreduce the original image

    Parameters
    ----------
    dir_path : String
        path to dir containing all tiles.
    choice : int, optional
        the stitching of two tiles can be used in  three ways:
            0 if we want to use to replace every pixle  of the tile in the
            back with the tile in the front 
            
            1 each matching pixle in the crossover between two tile are used
            as input to OR operation and the result is in final image
            
            2 each matching pixle in the crossover between two tile are used
            as input to AND operation and the result is in final image

    Returns
    -------
    None.

    """
    
    directory = dir_path
    p_list = []
    
    #extracting x, y of each tile and adding it to an array
    for filename in os.listdir(directory):
        
        tmp = (filename.split(".")[0]).split('_')
        p_list.append((int(tmp[-2]),int(tmp[-1])))
        
    #extract maximum and minimum  x , y to calculate original image 
    #height and width
    max_x = max(p_list)[0]
    min_x = min(p_list)[0]
    max_y = max(p_list)[1]
    min_y = min(p_list)[1]
    
    
    # we take a sample to extract tile information such as height, width, type
    # original image name
    sample = os.listdir(directory)[0]  
    
    im = Image.open(dir_path + '\\' + sample)

    tile_h = np.array(im).shape[0]
    tile_w = np.array(im).shape[1]
    file_type = sample.split(".")[-1]
    original_name = ((sample[::-1]).split("_", 2))[-1][::-1]

    
    Original_width  = int((max_x - min_x + tile_w)/pixel_size)
    Original_height = int((max_y - min_y + tile_h)/pixel_size)

    #we create an NumPy array to stitch all tiles to.
    if(in_canels == 1):
        if choice == 2:     # if we choose AND
            output_array = np.ones((Original_height, Original_width))
        else:               # if we choose OR,  replace
            output_array = np.zeros((Original_height, Original_width))
    else:
        if choice == 2:     # if we choose AND
            output_array = np.ones((Original_height, Original_width , in_canels))
        else:               # if we choose OR,  replace
            output_array = np.zeros((Original_height, Original_width , in_canels))

    for filename in os.listdir(directory):

        #extraxt x, y of tile relative to original
        tmp = (filename.split(".")[0]).split('_')
        x = int((int(tmp[-2]) - min_x)/pixel_size)
        y = int((int(tmp[-1]) - min_y)/pixel_size)
        print(str(x)+", "+str(y))

        im = Image.open(dir_path + '\\' + filename)
        
        #copy tile  to output array, based on copying methid choosen
        if(in_canels == 1):
            if choice == 0:
                output_array[y:y + tile_h, x:x + tile_w] = np.array(im)
            elif choice == 1:
                output_array[y:y + tile_h, x:x + tile_w] = np.logical_or(
                    output_array[y:y + tile_h, x:x + tile_w], np.array(im))
            elif choice == 2:
                output_array[y:y + tile_h, x:x + tile_w] = np.logical_and(
                    output_array[y:y + tile_h, x:x + tile_w], np.array(im))
        else:
            if choice == 0:
                output_array[y:y + tile_h, x:x + tile_w, :] = np.array(im)
            elif choice == 1:
                output_array[y:y + tile_h, x:x + tile_w, :] = np.logical_or(
                     np.array(im) , output_array[y:y + tile_h, x:x + tile_w, :])
            elif choice == 2:
                output_array[y:y + tile_h, x:x + tile_w, :] = np.logical_and(
                    output_array[y:y + tile_h, x:x + tile_w, :], np.array(im))
            
    # converting array to image and saving image
    output_im = Image.fromarray(output_array)
    file_name = original_name+ "." + file_type
    path = save_path + '\\' + file_name
    output_im.save(path)

    
if __name__ == '__main__':    
        # this lines will run only if we are running this file directly
        # if we import the module then it will be ignored
        imgs_dir= r"C:\Users\Abed\Desktop\Tel aviv internship\Github\TreeDetection\Abed\experiements\pred_Unet"
        stitch(imgs_dir,imgs_dir,0.2, choice=0 )
