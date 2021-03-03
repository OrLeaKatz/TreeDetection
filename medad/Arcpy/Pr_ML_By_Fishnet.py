# -*- coding: utf-8 -*-

import os
import arcpy
import sys
from arcpy.sa import *
arcpy.env.overwriteOutput = True
import math 


def print_arcpy_message(msg, status=1):
    '''
    return a message :

    print_arcpy_message('sample ... text',status = 1)
    >>> [info][08:59] sample...text
    '''
    msg = str (msg)

    if status == 1:
        prefix = '[info]'
        msg = prefix + str (datetime.datetime.now ()) + "  " + msg
        print (msg)
        arcpy.AddMessage (msg)

    if status == 2:
        prefix = '[!warning!]'
        msg = prefix + str (datetime.datetime.now ()) + "  " + msg
        print (msg)
        arcpy.AddWarning (msg)

    if status == 0:
        prefix = '[!!!err!!!]'

        msg = prefix + str (datetime.datetime.now ()) + "  " + msg
        print (msg)
        arcpy.AddWarning (msg)
        msg = prefix + str (datetime.datetime.now ()) + "  " + msg
        print (msg)
        arcpy.AddWarning (msg)

        warning = arcpy.GetMessages (1)
        error = arcpy.GetMessages (2)
        arcpy.AddWarning (warning)
        arcpy.AddWarning (error)

    if status == 3:
        prefix = '[!FINISH!]'
        msg = prefix + str (datetime.datetime.now ()) + " " + msg
        print (msg)
        arcpy.AddWarning (msg)

def add_field(fc,field,Type = 'TEXT'):
    TYPE = [i.name for i in arcpy.ListFields(fc) if i.name == field]
    if not TYPE:
        arcpy.AddField_management (fc, field, Type)

def Making_fish_net(poly_mask,raster,Fish_net):

    desc_mask  = arcpy.Describe(poly_mask)
    S_R_mask  = desc_mask.spatialReference

    if desc_mask.ShapeType <> u'Polygon':
        print ("layer mask have to be in Type Polygon")
        sys.exit()

    cell_size   = float(str(arcpy.GetRasterProperties_management (raster, "CELLSIZEX")))
    pix_per_Gil = 500
    cul_size    = int(pix_per_Gil*cell_size)

    dic1 = {'Xmin':'','Xmax':'','Ymin':'','Ymax':''}
    for raw in arcpy.da.SearchCursor(poly_mask,["SHAPE@"]):
            extent_curr = raw[0].extent
            dic1['Xmin'] = (int(extent_curr.XMin))
            dic1['Xmax'] = (int(extent_curr.XMax))
            dic1['Ymin'] = (int(extent_curr.YMin))
            dic1['Ymax'] = (int(extent_curr.YMax))

    arcpy.AddMessage ("starting ... making fish net..1...2....3")
    arcpy.CreateFishnet_management(Fish_net, str(dic1['Xmin']) +" "+ str(dic1['Ymin']), str(dic1['Xmin']) + " "+str(dic1['Ymax']), str(cul_size), str(cul_size),"","", str(dic1['Xmax']) +" "+ str(dic1['Ymax']), "NO_LABELS", poly_mask, "POLYGON")

    arcpy.MakeFeatureLayer_management      (Fish_net,"Fish_net_lyr"             )
    arcpy.SelectLayerByLocation_management ("Fish_net_lyr","INTERSECT",poly_mask)
    arcpy.SelectLayerByAttribute_management("Fish_net_lyr","SWITCH_SELECTION"   )
    arcpy.DeleteFeatures_management        ("Fish_net_lyr"                      )

    fields = ['Xmin','Xmax','Ymin','Ymax']
    for i in fields:
        add_field(Fish_net,i,Type = 'DOUBLE')

    with arcpy.da.UpdateCursor(Fish_net,['Xmin','Xmax','Ymin','Ymax','SHAPE@'])as cursor:
        for row in cursor:
            extent = row[-1].extent
            row[0] = int(extent.XMin)
            row[1] = int(extent.XMax)
            row[2] = int(extent.YMin)
            row[3] = int(extent.YMax)
            cursor.updateRow(row)
    
    return Fish_net

def round_down(n,decimals = 0):
    multiplier = 10** decimals
    return math.floor(n*multiplier)/multiplier

def Cut_Raster_By_Fish_net(raster,Fish_net,exists_list,gdb):
    Spatial_ref                       = arcpy.Describe(raster).spatialReference
    arcpy.DefineProjection_management (Fish_net,Spatial_ref)

    oid_fieldname   = str(arcpy.Describe(Fish_net).OIDFieldName)
    data            = [[i[0],i[1]] for i in arcpy.da.SearchCursor(Fish_net,['SHAPE@',oid_fieldname])]

    for i in data:
        geom     = i[0]
        id_fish  = i[1]
        extent   = geom.extent
        name_x_y = str(int(extent.XMin)) +'_'+ str(int(extent.YMax))

        if id_fish in exists_list:
            tif_name_a    = gdb +"\\"+"ID_{}".format(str(name_x_y))
            out_put_ras = tif_name_a
            #print 'working on: {}'.format(str(id_fish))
            if arcpy.Exists(out_put_ras):
                arcpy.Delete_management(out_put_ras)
            print "{} {} {} {}".format(int(extent.XMin),int(extent.YMin),int(extent.XMax),int(extent.YMax))
            print geom.extent
            arcpy.Clip_management(raster,"{} {} {} {}".format(int(extent.XMin),int(extent.YMin),int(extent.XMax),int(extent.YMax)), out_put_ras, "" , "0", "NONE", "NO_MAINTAIN_EXTENT") # change for later



def Create_polygon_from_raster(Ras):
    outFile = 'in_memory' + '\\' + 'Layer'
    arcpy.CreateFeatureclass_management (os.path.dirname (outFile), os.path.basename (outFile), "POLYGON")
    cursor = arcpy.InsertCursor (outFile)
    point = arcpy.Point ()
    array = arcpy.Array ()
    corners = ["lowerLeft", "lowerRight", "upperRight", "upperLeft"]
    feat = cursor.newRow ()
    r = arcpy.Raster (Ras)
    for corner in corners:
                    point.X = getattr (r.extent, "%s" % corner).X
                    point.Y = getattr (r.extent, "%s" % corner).Y
                    array.add (point)
    array.add (array.getObject (0))
    polygon = arcpy.Polygon (array)
    feat.shape = polygon
    cursor.insertRow (feat)
    array.removeAll ()

    return outFile


def CheckIfMade(fishnet,build):

    name = "FID_" + os.path.basename(fishnet)
    if build != '':
        inter = 'in_memory' + '\\' + 'Inter'
        diss  = 'in_memory' + '\\' + 'Diss'

        arcpy.Intersect_analysis  ([fishnet,build],inter)
        arcpy.Dissolve_management (inter,diss,name)
        data = [i[0] for i in arcpy.da.SearchCursor(diss,[name,'SHAPE@AREA']) if i[1] > 1000]
    else:
        oid_fieldname   = str(arcpy.Describe(Fish_net).OIDFieldName)
        data            = [i[0] for i in arcpy.da.SearchCursor(fishnet,[oid_fieldname])]

    return data

def Del_none_value_ras(gdb):

    arcpy.env.workspace = gdb
    list1 = arcpy.ListDatasets()

    for ras in list1:
        inRas   = arcpy.Raster (ras)
        arr     = arcpy.RasterToNumPyArray (inRas, nodata_to_value=0)
        sum_ras = sum(arr.flatten())
        print ras
        print (sum_ras)
        if sum_ras < 5000:
            print "Delete: {}".format(ras)
            arcpy.Delete_management(ras)

def add_field(fc,field,Type = 'TEXT'):
    TYPE = [i.name for i in arcpy.ListFields(fc) if i.name == field]
    if not TYPE:
        arcpy.AddField_management (fc, field, Type)

def making_binary_raster(build,ortho_ras,mask,out_put):

    from arcpy.sa import *

    list_mask = []
    with arcpy.da.SearchCursor(mask,['SHAPE@'])as cursor:
        for row in cursor:
            extent = row[-1].extent
            list_mask.append([extent.XMin,extent.YMin,extent.XMax,extent.YMax])

    list_mask = list_mask[0]
    arcpy.env.extent = arcpy.Extent(list_mask[0],list_mask[1],list_mask[2],list_mask[3])

    cell_size   = float(str(arcpy.GetRasterProperties_management (ortho_ras, "CELLSIZEX")))

    gdb      = os.path.dirname(build)
    temp_ras = gdb + '\\' + 'raster'
    add_field                        (build,'CLASS','TEXT')
    arcpy.CalculateField_management  (build,"CLASS", "1", "VB", "")
    arcpy.FeatureToRaster_conversion (build,"CLASS",temp_ras,cell_size)

    arcpy.CheckOutExtension('Spatial')
    outIsNull = IsNull(temp_ras)
    #outIsNull = Reclassify(outIsNull,"Value",RemapValue([[0,1],[1,0]]))
    outIsNull.save(out_put)
    arcpy.Delete_management(temp_ras)
    

def createFolder(dic):
    try:
        if not os.path.exists(dic):
            os.makedirs(dic)
    except OSError:
        print ("Error Create dic")   

def Export_to_tif(gdb,type_ras = '',folder = ''):

    if type_ras == '':
        type_ras = 'Raster'

    if folder == '':
        area = os.path.dirname(gdb)
        folder = area + '\\' + str(type_ras)
        createFolder(folder)
        print "No folder giving, defualt is: {}".format(folder)

    arcpy.env.workspace = gdb
    list_ras = arcpy.ListDatasets()
    for i in list_ras:
        name = folder + '\\' +str(i) + '_' + str(type_ras) + '.tif'
        print "Doing: {}".format(name)
        arcpy.CopyRaster_management(i , name)

    return folder


def Fix_fodler_raster(Fodler):
    already_exists = []
    for root,dirs,files in os.walk(Fodler):
        for file in files:
            if file.endswith('.tif') or file.endswith('.tfw'):
                try:
                    index_num   = file.index('_',12)
                    name        = file[0:index_num]

                    old         = root + '\\' + file
                    after_point = file.split('.')[-1]
                    new = root + '\\' + name + '.' + after_point
                    try:
                        print "old name: {},  New Name: {}".format(file.split('.')[0],name)
                        os.rename(old,new)
                    except:
                        pass
                except:
                    pass
            else:
                print "File {}, removed".format(root + '\\' + file)
                os.remove(root + '\\' + file)



# in Puts
ortho_ras  = r"F:\medad\Python_tools\ML_For_moshe\data\UFH-1819_ITM_20cm_NCNZ.tif" # input, orthopoto 
build      = r'F:\medad\Python_tools\ML_For_moshe\data\layers.gdb\Building'    # input - layer of all the samples for ML
mask       = r''                                                                   # input - optional - make fish net in this size, by defaul will take raster mask

# Work Space
gdb    = os.path.dirname (build)
Folder = os.path.dirname (gdb)

# Out Puts

gdb1       = Folder + '\\' +'orthophoto.gdb'
gdb2       = Folder + '\\' +'binary.gdb'
Fish_n     = gdb    + '\\' + 'Fish_net'
binary_ras = gdb    + '\\' + 'binary'


print_arcpy_message(" # # # S T A R T # # #", status=1)

if mask == '':
    mask    = Create_polygon_from_raster (ortho_ras)

if not arcpy.Exists(gdb1):
    gdb1 = arcpy.CreateFileGDB_management(Folder,'orthophoto.gdb')
    

if not arcpy.Exists(gdb2):
    gdb2 = arcpy.CreateFileGDB_management(Folder,'binary.gdb')


print_arcpy_message(" # # # Create binary raster # # #", status=1)
making_binary_raster                     (build,ortho_ras,mask,binary_ras)

print_arcpy_message(" # # # Create FISH NET # # #", status=1)
Fish_net    = Making_fish_net            (mask,ortho_ras,Fish_n)

print_arcpy_message(" # # # Check If buildings in cell # # #", status=1)
Exists_list = CheckIfMade                (Fish_n,build)
# cut source raster
print_arcpy_message(" # # # cut source raster # # #", status=1)
Cut_Raster_By_Fish_net                   (ortho_ras,Fish_net,Exists_list,gdb1)

print_arcpy_message(" # # # cut binary raster # # #", status=1)
Cut_Raster_By_Fish_net                   (binary_ras,Fish_net,Exists_list,gdb2)

print_arcpy_message(" # # # del empty binary raster # # #", status=1)
Del_none_value_ras                       (gdb2)

print_arcpy_message(" # # # Export Raster To Tif # # #", status=1)
fodler_RGB = Export_to_tif (gdb1,'RGB',folder)
fodler_bin = Export_to_tif (gdb2,'Binary',folder)

print_arcpy_message(" # # # Keep only Tif and tfw files, Change names currectly # # #", status=1)
Fix_fodler_raster(fodler_RGB)
Fix_fodler_raster(fodler_bin)


print_arcpy_message(" # # # F I N I S H # # #", status=1)

