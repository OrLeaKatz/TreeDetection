# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 07:48:23 2019

@author: medad
"""

import os
import gdalnumeric
from itertools import groupby
 
    
def Combine_dict(ListOfDict):
    '''
    input: List of dictionary: [{1: 10, 2: 20, 3: 30},{1: 10, 2: 20, 4: 30},{2: 20, 5: 30}]
    Out put:                   {1: 20, 2: 60, 3: 30, 4: 30, 5: 30}
    '''
    new_dic = {}
    for i in ListOfDict:
        for key, val in i.items():
            try:
                new_dic[key] += val
            except:
                new_dic[key] = val
    return new_dic


def Checking_Pix_count(folder):
    '''
    input:   folder contains tif files
    Out put: 1) count pix as txt file of every tif
             2) sum of all tif pix
    '''
    total = []   
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.tif'):
                path_raster = root + '\\' + file
                raster_file = gdalnumeric.LoadFile (path_raster)
                flat        = raster_file.flatten  ()
                data        = {value: len(list(freq)) for value, freq in groupby(sorted(flat))}
                text_path   =  path_raster.split('.')[0] + '_text.txt'
                text_file   = open(text_path, "w")
                text_file.write(str(data))
                total.append   (data)
                text_file.close()
                print ('in Put: '  + path_raster)
                print ('Out Put: ' + text_path)

    all_data    = Combine_dict(total)     
    exl_path    = folder +'\\'+ 'All_data.txt'
    text_file   = open(exl_path, "w")
    text_file.write(str(all_data))
                

folder = r'C:\GIS_layers\raster\DEM DSM\Raster_DTM_RSH'
Checking_Pix_count(folder)


