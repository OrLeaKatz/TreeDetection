import os
from PIL import Image
import numpy as np
import re

# import sys
# rootdir = r"C:\Users\abed\Desktop\func"
# sys.path.append(rootdir)

folder_path = r"C:\Users\Abed\Desktop\Tel aviv internship\functions i made\img_crops"
original_img_xy_re = ".*_(\d+)_(\d+)"
tiles_xy_re = ".*__(\d+)_(\d+)__"


# three options and=2 , or=1 , replace = 0
def stitch(dir_path, choice=0):
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

    tile_h, tile_w, _ = np.array(im).shape
    file_type = first.split(".")[-1]

    # creating array to merge all tiles to
    if choice == 2:  # if we choose and
        output_array = np.ones((Original_height, Original_width, 3))
    else:
        output_array = np.zeros((Original_height, Original_width, 3))

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

    array = sorted(array, key=lambda k: [k[0], k[1]])
    numpy_array = np.array(array)
    matrix = numpy_array.reshape(sum_of_files // tiles_horizontal_num,
                                 tiles_horizontal_num, 2)


stitch(folder_path, 0)
