import os
from PIL import Image
import numpy as np
import re


def calcul_xyz_array(img_x, img_y, tile_x, tile_y, cross_x=0, cross_y=0):
    """
    calcul_xyz_array
    
    function calculates xy point to crop image according  to varios parameters

    Parameters
    ----------
    img_x : int
        original image width
    img_y : itt
        original image height
    tile_x : int
        outpud image width
    tile_y : int
        outpud image height
    cross_x : int
        how many pixels to overlap between talies in width
    cross_y : int
        how many pixels to overlap between talies in height

    Returns
    -------
    array : Array of tuples
        array cotaining all points of (x,y) to crop.

    """
    array = []

    modu_x = cross_x
    modu_y = cross_y
    current_x = 0
    current_y = 0

    while current_y + tile_y <= img_y:

        while current_x + tile_x <= img_x:

            array.append((current_x, current_y))

            if current_x + tile_x == img_x:
                break

            current_x += tile_x

            if current_x + tile_x > img_x:  # we reached end of x

                array.append((img_x - tile_x, current_y))
                break
            if current_x == tile_x:
                current_x += - modu_x

        current_x = 0   # new line
        if current_y + tile_y == img_y:
            break

        current_y += tile_y

        if current_y + tile_y > img_y:  # we reached end of y

            current_y = img_y - tile_y
            continue

        if current_y == tile_y:
            current_y += - modu_y

    return array


def calcul_xy_array(img_x, img_y, tile_x, tile_y):
    """
    calcul_xy_array
    
    function calculates xy point to crop image according  to varios parameters
    this function empisizses  minimal crops

    Parameters
    ----------
    img_x : int
        original image width
    img_y : itt
        original image height
    tile_x : int
        outpud image width
    tile_y : int
        outpud image height

    Returns
    -------
    array : Array of tuples
        array cotaining all points of (x,y) to crop.

    """
    array = []

    modu_x = img_x % tile_x
    modu_y = img_y % tile_y
    div_x = img_x // tile_x
    div_y = img_y // tile_y
    current_x = 0
    current_y = 0

    for i in range(div_y):
        for j in range(div_x):
            array.append((current_x, current_y))
            current_x += tile_x
        if modu_x:
            array.append((img_x - tile_x, current_y))
        current_y += tile_y
        current_x = 0

    if modu_y:
        current_y = img_y - tile_y
        for j in range(div_x):
            array.append((current_x, current_y))
            current_x += tile_x
        if modu_x:
            array.append((img_x - tile_x, current_y))

    return array


def crop_img(img_path, tile_x, tile_y , save_path):
    """
    crop_img
    
    crops image  to multiples tiles according to input

    Parameters
    ----------
    img_path : string
        full image path to crop.
    tile_x : int
        outpud image width.
    tile_y : int
        outpud image height.
    save_path : save
        a path to save all crops of image.

    Returns
    -------
    None.

    """
    # make directory to save tiles
    im = Image.open(img_path)
    try:
        os.mkdir(img_path)
    except OSError:
        print("Creation of the directory %s failed" % img_path)
    else:
        print("Successfully created the directory %s " % img_path)
    
    # conver image to numpyarray and extract image height and width
    img_arr = np.array(im)
    shape = img_arr.shape
    img_y = shape[0]
    img_x = shape[1]

    #calculate point to crop
    xy_points = calcul_xy_array(img_x, img_y, tile_x, tile_y)

    for x, y in xy_points:
        
        #extract pixels fro array
        A = img_arr[y: y + tile_y, x: x + tile_x, :]
        
        #convert array back to img
        im = Image.fromarray(A)


        #saving the image in formate:
        #Original_img_name + "__" + tile_x_cor "_" + tile_y_cor "__"+
        #Original_img_height + "_" + Original_img_width
        name = (img_path.split('\\'))[-1]
        file_name = str(name) + "__" + str(x) + "_" + str(y) + "__" + str(
            img_x) + "_" + str(img_y) + ".tif"

        path = save_path + '\\' + file_name
        im.save(path)
       
        
        
        
        
original_img_xy_re = ".*_(\d+)_(\d+)"
tiles_xy_re = ".*__(\d+)_(\d+)__"
        
# three options and=2 , or=1 , replace = 0
def stitch(dir_path, in_canels=1, choice=0):
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
    array = []  # array used to create matrix

    p = re.compile(tiles_xy_re)
    q = re.compile(original_img_xy_re)

    sum_of_files = len(os.listdir(directory))
    tiles_horizontal_num = 0

    first = os.listdir(directory)[0]  # we take a sample to extract
    # original image information such as height, width, type

    original = q.match(first)
    Original_width, Original_height = int(original.group(1)), int(
        original.group(2))
    im = Image.open(dir_path + '\\' + first)

    tile_h = np.array(im).shape[0]
    tile_w= np.array(im).shape[1]
    file_type = first.split(".")[-1]

    # creating array to merge all tiles to
    if choice == 2:  # if we choose and
        output_array = np.ones((Original_height, Original_width, in_canels))
    else:
        output_array = np.zeros((Original_height, Original_width, in_canels))

    for filename in os.listdir(directory):

        xy = p.match(filename)
        x, y = int(xy.group(1)), int(xy.group(2))  # extracting x,y relative
        # to original img

        im = Image.open(dir_path + '\\' + filename)
        if choice == 0:
            output_array[y:y + tile_h, x:x + tile_w, :] = np.array(im)
        elif choice == 1:
            output_array[y:y + tile_h, x:x + tile_w, :] = np.logical_or(
                output_array[y:y + tile_h, x:x + tile_w, :], np.array(im))
        elif choice == 2:
            output_array[y:y + tile_h, x:x + tile_w, :] = np.logical_and(
                output_array[y:y + tile_h, x:x + tile_w, :], np.array(im))

        output_array[y:y + tile_h, x:x + tile_w, :] = np.array(im)

        array.append([x, y])

        if int(xy.group(1)) == 0:
            tiles_horizontal_num = tiles_horizontal_num + 1

    # converting array to image and saving image
    output_im = Image.fromarray(output_array.astype(np.uint8))
    file_name = "original." + file_type
    path = dir_path + '\\' + file_name
    output_im.save(path)

    # array = sorted(array, key=lambda k: [k[0], k[1]])
    # numpy_array = np.array(array)
    # matrix = numpy_array.reshape(sum_of_files // tiles_horizontal_num,
    #                              tiles_horizontal_num, 2)
    
    
    
if __name__ == '__main__':
    
    imgs_dir= r"C:\Users\abed\Desktop\project\func\Model\pred_Unet"

    stitch(imgs_dir,1)

    