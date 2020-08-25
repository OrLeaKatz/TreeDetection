import numpy as np
import geopandas as gpd
from osgeo import ogr
from osgeo import gdal
import os,osr
import json



"""Creates a point layer from vertices in a line layer."""

path        = r'C:\GIS_layers\Vector\Corona_saminar\Export_Output.shp'
ras         = r'C:\GIS_layers\Vector\Corona_saminar\Sum_Value_diff_norm1.tif'
out_put     = r'C:\GIS_layers\Vector\Corona_saminar\Out_put.shp'
json_path   = r'C:\GIS_layers\Vector\Corona_saminar\COCO_ME.json'

ds_ras           = gdal.Open( ras )
geotransform = ds_ras.GetGeoTransform()
ulx          = geotransform[0]                         # נקודה שמאלית עליונה X
uly          = geotransform[3]                         # נקודה שמאלית עליונה Y

source   = ogr.Open(path,update=True)
layer    = source.GetLayer()
sr       = layer.GetSpatialRef()

drv     = ogr.GetDriverByName('ESRI Shapefile')
out_ds  = drv.CreateDataSource(out_put)
out_lyr = out_ds.CreateLayer('name', sr, ogr.wkbPolygon)
defn = out_lyr.GetLayerDefn()

multi = ogr.Geometry(ogr.wkbMultiPolygon)

for yard in layer:
    ring = yard.GetGeometryRef()
    num = 0
    #print (str(ring)[:20])
    for part in ring:
        for i in range(part.GetPointCount()): 
            part.SetPoint(i, part.GetX(i)-ulx, part.GetY(i)-uly)
            num +=1
        #print (num)

    wkt = ring.ExportToWkt()
    multi.AddGeometryDirectly(ogr.CreateGeometryFromWkt(wkt))

union = multi.UnionCascaded()

out_feat = ogr.Feature(defn)
out_feat.SetGeometry(union)
out_lyr.CreateFeature(out_feat)
out_ds.Destroy()
    

driver = ogr.GetDriverByName('ESRI Shapefile')
data_source = driver.Open(out_put, 0)

fc = {
    'features': []
    }

lyr = data_source.GetLayer(0)
for feature in lyr:    
    fc['features'].append(feature.ExportToJson(as_object=True))

with open(json_path, 'w') as f:
    json.dump(fc, f)
