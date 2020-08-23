# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 07:48:23 2019

@author: medad
"""

import os
from osgeo import gdal
import numpy as np
import osgeo.ogr as ogr
from osgeo import gdalconst
import subprocess


def createFolder(path):
	path2 = os.path.dirname(path)
	print (path2)
	try:
		dic2 = path2 +'\\'+ 'TrainSet'
		if not os.path.exists(dic2):
			os.makedirs(dic2)
			print ('Createrd folder {}'.format(dic2))
		else:
			print ('folder {} is already created'.format(dic2))
	except OSError:
		print ("Error Create dic")
        
	return dic2
        

def avr_bands(in_ds):
    
    name = os.path.basename(in_ds).split('.')[0]
    out = os.path.dirname(in_ds) + '\\'+name+'_gray.tif'
    in_ds = gdal.Open(in_ds)
    num_bands = in_ds.RasterCount
    band1 = in_ds.GetRasterBand(1)    
    band2 = in_ds.GetRasterBand(2) 
    band3 = in_ds.GetRasterBand(3)
    red       = band1.ReadAsArray()*0.3
    blue      = band3.ReadAsArray()*0.11
    if num_bands == 4:
        band4 = in_ds.GetRasterBand(4)
        green_inf = np.mean([band2.ReadAsArray(),band4.ReadAsArray()],axis = 0)*0.59
    else:
        print ("didn't find the 4th band")
        green_inf = np.mean([band2.ReadAsArray()],axis = 0)*0.59
        
    new_array = np.sum([green_inf,blue,red],axis = 0)
    driver    = gdal.GetDriverByName('GTiff')
    out_ds    = driver.Create(out, in_ds.RasterXSize, in_ds.RasterYSize, 1, gdal.GDT_CFloat64)
    
    out_ds.SetProjection  (in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    
    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray            (new_array)
    out_band.FlushCache            ()
    out_ds.FlushCache              ()

    return out


def get_img_shp(folder):
    img = []
    shp = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('tif'):
                img.append(root +'\\' + file)
            if file.endswith('shp'):
                shp.append(root +'\\' + file)
                
                
    return shp,img


def Cut_raster_to_pices(path_raster,out_put_folder,name = 'None',tilesize = 512):
    
    in_ds = gdal.Open(path_raster)
    width  = in_ds.RasterXSize
    height = in_ds.RasterYSize

    for i in range(0,width,tilesize):
        for j in range(0,height,tilesize):
            w = tilesize
            h = tilesize
            gdaltranString = "gdal_translate -of GTIFF -srcwin "+str(i)+", "+str(j)+", "+str(w)+", " \
                +str(h)+" " + path_raster + " " + out_put_folder + "\\_"+ str(name) +str(i)+"_"+str(j)+".tif"
            os.system(gdaltranString)


def del_ras(folder,by_name):
    delete = 0
    no_del = 0
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('tif'):
                if by_name in file:
                    try:
                        os.remove(root +'\\' + file)
                        delete += 1
                    except:
                        print ('coudnt delete: {}'.format(root +'\\' + file))
                        no_del += 1
    print ('total deleted: {}'.format(delete))
    print ('total coudnt deleted: {}'.format(no_del))

def RasterRize_gdal(ndsm,shp,output):
    

    data = gdal.Open(ndsm, gdalconst.GA_ReadOnly)
    geo_transform = data.GetGeoTransform()
    
    x_min = geo_transform[0]
    y_max = geo_transform[3]
    y_min = y_max + geo_transform[5] * data.RasterYSize
    x_res = data.RasterXSize
    y_res = data.RasterYSize
    mb_v = ogr.Open(shp)
    mb_l = mb_v.GetLayer()
    pixel_width = geo_transform[1]
    
    target_ds = gdal.GetDriverByName('GTiff').Create(output, x_res, y_res, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixel_width, 0, y_min, 0, pixel_width))
    band = target_ds.GetRasterBand(1)
    NoData_value = -999999
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    gdal.RasterizeLayer(target_ds, [1], mb_l, options=["ATTRIBUTE=Class_num"])
    
    target_ds = None
    
    return output


def del_zero_value_in_raster(folder):
    rasters = []
    file_type  = r'tif'
    
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(file_type):
                rasters.append(root +'\\'+f)
                
    
    for ras in rasters:
        raster = gdal.Open(ras)
        
        
        num_bands = raster.RasterCount
        
        num = 0
        for i in range(1,num_bands+1):
            band       = raster.GetRasterBand(i)
            band_array = band.ReadAsArray()
            mean_band  = np.mean(band_array)
            num += mean_band
        
        del raster
        del band
        del band_array
        del mean_band
        
        if num == 0:
            os.remove(ras)
            print ("deleted {} because of no value".format(ras))
        else:
            pass
            #print ("{} have_value".format(ras))



def get_list_of_Values(shp_in,attri):
    driver     = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(shp_in,0)
    layer      = dataSource.GetLayer()
    list_field = [attri]
    value_list = []
    for feature in layer:
        value_list.append([feature.GetField(j) for j in list_field][0])
        
    value_list = list(set(value_list))
    return value_list


def RasterizShape_subprocess(shp_in,img_ref,name):

    print (os.path.dirname(shp_in) + '\\' + 'LBL_{}.tif'.format(str(name)))
    img_out = os.path.dirname(shp_in) + '\\' + 'LBL_{}.tif'.format(str(name))
    
    img_ref        = gdal.Open(img_ref)
    img_ref_cols   = img_ref.RasterXSize
    img_ref_rows   = img_ref.RasterYSize
    geotransform   = img_ref.GetGeoTransform()
    top_left_X     = geotransform[0]
    pixel_size     = float(geotransform[1]) # pixel size in the X direction
    top_left_Y     = geotransform[3]
    xmin = top_left_X
    ymin = top_left_Y - img_ref_rows*pixel_size
    xmax = top_left_X + img_ref_cols*pixel_size
    ymax = top_left_Y 

    print ("[info]runing the tool")
    subprocess.call('gdal_rasterize --config GDAL_CACHEMAX 10000 -ot Byte -te {} {} {} {} -tr {} {} -a CLASS {} {} -where "Class_num = {}"'.format(xmin,str(name)),shell = True)
    
    return img_out



shp_path     = r'C:\Users\medad\python\GIStools\TREES\data\Pre_ML\Sample_3.shp'
raster_path  = r"C:\GIS_layers\raster\ortho\RSH-1231_ITM_20cm_CNZ.tif"

folder  = createFolder(shp_path)
#Cut_raster_to_pices(raster_path,folder,name = 'None',tilesize = 512)

name_ras = os.path.dirname(folder) + '\\' +'rastarize_shp.tif'
RasterRize_gdal(raster_path,shp_path,name_ras)
     
Cut_raster_to_pices(name_ras,folder,name = 'ras_shp_',tilesize = 512)


#shps,imgs = get_img_shp(folder)
#num = 0
#for img in imgs:
#    try:
#        if 'gray' not in img:
#            avr_bands(img)
#            if num%10 == 0:
#                print (num)
#            
#            num +=1
#    except:
#        print ("coudnt make: {} ".format(img))
##    
#
#list_val = get_list_of_Values(shp_path,'CLASS')
#list_val = [15,31,7]
#for val in list_val:
#    print (' # # working on {} # # '.format(val))
#    img_out = RasterizShape_subprocess     (shp_path,raster_path,str(val))
#    Cut_raster_to_pices(img_out,folder,name = 'LBL_'+ str(val) +'_',tilesize = 512)
#

del_zero_value_in_raster(folder)

