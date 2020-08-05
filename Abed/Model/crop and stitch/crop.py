import sys
import os
from calculacte_xy import calcul_xy_array
from PIL import Image
import numpy as np


def crop_img(img_path, tile_x, tile_y , save_path):
    # make directory to save tiles
    im = Image.open(img_path)
    try:
        os.mkdir(img_path)
    except OSError:
        print("Creation of the directory %s failed" % img_path)
    else:
        print("Successfully created the directory %s " % img_path)

    img_arr = np.array(im)
    shape = img_arr.shape
    img_y = shape[0]
    img_x = shape[1]

    xy_points = calcul_xy_array(img_x, img_y, tile_x, tile_y)

    for x, y in xy_points:

        A = img_arr[y: y + tile_y, x: x + tile_x, :]
        im = Image.fromarray(A)

        name = (img_path.split('\\'))[-1]
        file_name = str(name) + "__" + str(x) + "_" + str(y) + "__" + str(
            img_x) + "_" + str(img_y) + ".tif"

        path = save_path + '\\' + file_name
        im.save(path)


# def crop_tif(img_path, tile_x, tile_y):
#     path = "img_crops"
#     try:
#         os.mkdir(path)
#     except OSError:
#         print("Creation of the directory %s failed" % path)
#     else:
#         print("Successfully created the directory %s " % path)
#
#     f = np.memmap(img_path, dtype=np.uint32, mode='r', shape=(5000, 5000))
#     img_arr = np.array(f)
#     shape = img_arr.shape
#     print(shape)


#path1 = r"\\gesher6-rx\From_Yitzuri\moshey\RSH-1231_ITM_20cm_CNZ_16.TIF"
path = r"ort3.png"
tile_x, tile_y = (500, 500)
crop_img(path, tile_x, tile_y)
