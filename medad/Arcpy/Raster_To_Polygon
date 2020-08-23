# -*- coding: utf-8 -*-
import os
import arcpy
import numpy as np
import datetime
import csv
import gc

arcpy.env.overwriteOutput = True

def print_arcpy_message(msg,status = 1):
    '''
    return a message :
    
    print_arcpy_message('sample ... text',status = 1)
    >>> [info][08:59] sample...text
    '''
    msg = str(msg)
    
    if status == 1:
        prefix = '[info]'
        msg = prefix + str(datetime.datetime.now()) +"  "+ msg
        print (msg)
        arcpy.AddMessage(msg)
        
    if status == 2 :
        prefix = '[!warning!]'
        msg = prefix + str(datetime.datetime.now()) +"  "+ msg
        print (msg)
        arcpy.AddWarning(msg)
        
    if status == 0 :
        prefix = '[!!!err!!!]'
        
        msg = prefix + str(datetime.datetime.now()) +"  "+ msg
        print (msg)
        arcpy.AddWarning(msg)
        msg = prefix + str(datetime.datetime.now()) +"  "+ msg
        print (msg)
        arcpy.AddWarning(msg)
        
        warning = arcpy.GetMessages(1)
        error   = arcpy.GetMessages(2)
        arcpy.AddWarning(warning)
        arcpy.AddWarning(error)
        
    if status == 3 :
        prefix = '[!FINISH!]'
        msg = prefix + str(datetime.datetime.now()) + " " + msg
        print (msg)
        arcpy.AddWarning(msg)


def del_field_list(fc_to_delete_fields_from, list_of_fileds_to_del):    
        field_names = [f.name for f in arcpy.ListFields(fc_to_delete_fields_from)]
        for field in field_names:
                if field in list_of_fileds_to_del:
                        try:
                                arcpy.DeleteField_management(fc_to_delete_fields_from, field)
                        except:
                                print field + " Can't be deleted"
        pass



def add_field(fc,field,Type = 'TEXT'):
    TYPE = [i.name for i in arcpy.ListFields(fc) if i.name == field]
    if not TYPE:
        arcpy.AddField_management (fc, field, Type)


def Get_False_Type(predict_shp,shp_orig):

    add_field                              (predict_shp,'False_Type','TEXT')
    arcpy.MakeFeatureLayer_management      (predict_shp,'predict_shp_lyr')
    arcpy.SelectLayerByLocation_management ('predict_shp_lyr','INTERSECT',shp_orig,'',"NEW_SELECTION","INVERT")

    num = 0
    with arcpy.da.UpdateCursor('predict_shp_lyr',['False_Type']) as cursor:
        for raw in cursor:
            raw[0] = 'False_nagative'
            num += 1
            cursor.updateRow(raw)
    del cursor
    return num


def Raster_to_Shape(path,gdb):

    polygon      = gdb + '\\'+'polygon'
    predict_shp  = gdb + '\\' + 'predict_shp'
    temp_buffer1 = r'in_memory\bufferIN1'
    temp_buffer2 = r'in_memory\bufferIN2'

    in_ras = arcpy.Raster(path)
    arr    = arcpy.RasterToNumPyArray(in_ras)
    arr2   = np.where(arr == 0,1,0)

    X          = getattr (in_ras.extent, "lowerLeft").X
    Y          = getattr (in_ras.extent, "lowerLeft").Y
    lower_left = arcpy.Point(X,Y)

    re_class = arcpy.NumPyArrayToRaster(arr2,lower_left,in_ras.meanCellWidth,in_ras.meanCellHeight)
    arcpy.RasterToPolygon_conversion   (re_class,polygon,"SIMPLIFY","VALUE")
    arcpy.MakeFeatureLayer_management  (polygon,'polygon_lyr',"\"gridcode\" = 0")
    arcpy.DeleteFeatures_management    ('polygon_lyr')

    # Delete Lines in prediction shp
    arcpy.Buffer_analysis                  (polygon,temp_buffer1,-0.5)
    arcpy.Buffer_analysis                  (temp_buffer1,temp_buffer2,0.5)
    arcpy.MultipartToSinglepart_management (temp_buffer2,predict_shp)
    arcpy.Delete_management                (polygon)

    return predict_shp

def create_Folder_GDB(dic):
    try:
        if not os.path.exists(dic):
            os.makedirs(dic)
    except OSError:
        print ("Error Create dic")   

    GDB_name = 'Predict_' + str(datetime.datetime.now())[0:10]
    gdb      = str(arcpy.CreateFileGDB_management(dic, str(GDB_name), "CURRENT"  ))
    return gdb

def createFolder(dic):
    try:
        if not os.path.exists(dic):
            os.makedirs(dic)
    except OSError:
        print ("Error Create dic")  


def Calc_Connection_Merge_Inter(BUILDING,BLDG_orig,gdb = ''):

        def accurancy(fc,field1,value = ''):

                accurancy = "accurancy" + str(value)
                arcpy.AddField_management (fc, accurancy, "TEXT")
                
                x = [row[0] for row in arcpy.da.SearchCursor (fc,[str(field1)])]
                
                with arcpy.da.UpdateCursor(fc,[field1, accurancy]) as cursor:
                        for row in cursor:
                                row[1] = x.count(row[0])
                                cursor.updateRow(row)

                return accurancy

        def Calculate_connection(fc,field_A,field_B):

                def calc_0_1_2_3_4(A,B):
                        num = 0
                        if int(A) == 1 and int(B) == 1:
                                num = 1
                        if int(A) == 1 and int(B) >1:
                                num = 2
                        if int(A) > 1 and int(B) == 1:
                                num =  3
                        if int(A) > 1 and int(B) > 1:
                                num =  4
                        return num
                        
                try:
                        arcpy.AddField_management (fc, 'Connection', "LONG")
                except:
                        pass
                with arcpy.da.UpdateCursor(fc,['Connection',field_A,field_B]) as Ucursor:
                        for row in Ucursor:
                                row[0] = calc_0_1_2_3_4(row[1],row[2])
                                Ucursor.updateRow(row)
                                
                                
        def del_field(fc_to_delete_fields_from, list_of_fileds_to_keep):    
                field_names = [f.name for f in arcpy.ListFields(fc_to_delete_fields_from)]
                for field in field_names:
                        if field not in list_of_fileds_to_keep:
                                try:
                                        arcpy.DeleteField_management(fc_to_delete_fields_from, field)
                                except:
                                        print field + " Can't be deleted"
                pass

        def Delete_layers_after_use(layers,True_False = True):
                if True_False:
                    for i in layers:
                                    try:
                                            arcpy.Delete_management (i)
                                    except:
                                        pass 
                
        if gdb == '':
            gdb    = os.path.dirname(BUILDING)
            
        BLDG   = gdb +'\\' +'BLDG_cut'

        Data     = gdb +'\\' + 'DATA'
        Data2    = gdb +'\\' + 'DATA2'
        Data4    = r'in_memory' +'\\' + 'DATA4'
        Data5    = gdb +'\\' + 'FINISH'

        BUILDING_me  = r'in_memory'  +'\\' + 'BUILDING_me'
        BUILDING_ti  = r'in_memory' +'\\' + 'BUILDING_ti'
        dis_BUILDING = r'in_memory' +'\\' + 'dis_BUILDING'
        dis_BLDG     = r'in_memory' +'\\' + 'dis_BLDG'

        merge        = r'in_memory' + '\\' + 'Merge'

        merge_dis    = r'in_memory' + '\\' + 'merge_dis'
        merge_sin    = gdb + '\\' + 'merge_sin'


        print_arcpy_message("   #    #    #      Prepare Data      #     #     #",status = 1)

        try:
                arcpy.AddField_management              (BLDG_orig, 'ID_BLDG', "DOUBLE"  )
                arcpy.CalculateField_management        (BLDG_orig, 'ID_BLDG', "[OBJECTID]", "VB", ""    )
        except:
                pass
        try:
                arcpy.AddField_management              (BLDG_orig, 'AREA_BLDG', "DOUBLE")
                arcpy.CalculateField_management        (BLDG_orig, "AREA_BLDG", "!SHAPE_Area!", "PYTHON")
        except:
                pass

        arcpy.MakeFeatureLayer_management      (BLDG_orig,'BLDG_orig_lyr')
        arcpy.SelectLayerByLocation_management ('BLDG_orig_lyr',"INTERSECT",BUILDING,'5 Meters')
        arcpy.Select_analysis                  ('BLDG_orig_lyr',BLDG)

        try:
                arcpy.DeleteField_management(BLDG_orig, 'ID_BLDG')
        except:
                pass

        try:
                arcpy.DeleteField_management(BLDG_orig, "AREA_BLDG")
        except:
                pass

        print_arcpy_message(" #    #    #    Prepare Connection     #     #     #",status = 1)
        
        field_BUILDING = 'FID_' + os.path.basename(BUILDING)
        field_BLDG     = 'FID_' + os.path.basename(BLDG)        


        arcpy.Intersect_analysis  ([BUILDING,BLDG],Data)
        accurancy1 = accurancy    (Data,field_BUILDING,'1')
        accurancy2 = accurancy    (Data,field_BLDG,'2')
        Calculate_connection      (Data,accurancy1,accurancy2)


        print_arcpy_message(" #    #    #    Create Area Of merge     #     #     #",status = 1)
        arcpy.Dissolve_management (BUILDING,dis_BUILDING)
        arcpy.Dissolve_management (BLDG,dis_BLDG)

        arcpy.Merge_management    ([dis_BUILDING,dis_BLDG],merge)


        arcpy.Dissolve_management              (merge,merge_dis)
        arcpy.MultipartToSinglepart_management (merge_dis,merge_sin)

        arcpy.AddField_management       (merge_sin, "AREA_Merge", "DOUBLE")
        arcpy.CalculateField_management (merge_sin, "AREA_Merge", "!SHAPE_Area!", "PYTHON")

        print_arcpy_message(" #    #    #    Create Area Of combine Intersect     #     #     #",status = 1)

        arcpy.SpatialJoin_analysis      (Data,merge_sin,Data2)
        arcpy.AddField_management       (Data2, 'Combine_Intersect', "DOUBLE")


        field_BLDG = os.path.basename(BLDG)
        list1 = [[row[0],row[1]] for row in arcpy.da.SearchCursor(Data2,['FID_'+field_BLDG,'SHAPE@AREA'])]
        dic = {}
        for i in list1:
                if i[0] in dic.keys():
                        dic[i[0]] = i[1] + dic[i[0]]
                else:
                        dic[i[0]] = i[1]


        with arcpy.da.UpdateCursor(Data2,['FID_'+field_BLDG,'Combine_Intersect']) as cursor:
                for row in cursor:
                        if dic.has_key(row[0]):
                                row[1] = dic[row[0]]
                                cursor.updateRow(row)

        print_arcpy_message(" #    #    #    Spatial Join      #     #     #",status = 1)

        arcpy.SpatialJoin_analysis  (Data2,merge_sin,Data4)
        del_field                   (Data4, ['Combine_Intersect','AREA_Merge','AREA_Intersect','Connection','ID_BLDG','AREA_BLDG'])
        arcpy.SpatialJoin_analysis  (BUILDING,Data4,Data5)

        print_arcpy_message(" #    #    #    Calculate   PRCT    #     #     #",status = 1)

        arcpy.AddField_management       (Data5, "PRCT", "DOUBLE")
        arcpy.CalculateField_management (Data5, 'PRCT', "(!Combine_Intersect!  / !AREA_Merge!) * 100", "PYTHON")
        arcpy.AddField_management       (Data5, "prec_Predict", "DOUBLE")
        arcpy.CalculateField_management (Data5, "prec_Predict",  "(!AREA_BLDG!  / !AREA_Merge!) * 100", "PYTHON")
        arcpy.AddField_management       (Data5, "prec_Sample", "DOUBLE")
        arcpy.CalculateField_management (Data5, "prec_Sample",  "(!SHAPE_Area!  / !AREA_Merge!) * 100", "PYTHON")

        print_arcpy_message(" #    #    #    Delete mid-layer    #     #     #",status = 1)

        Delete_layers_after_use([gdb +'\\' + 'BLDG_cut',gdb +'\\' + 'DATA2',gdb +'\\' + 'merge_sin',gdb +'\\' + 'DATA'],True)


        return Data5


def STDerror(lis1):
    
    """
    input: list of intersect over union prec
    list = [99,23,45,67,45]
    STDerror(list) = 24.3
    OutPut: STDerror of intersect over union prec 
    """
    
    def avr(list1):
        avr = sum(list1)/len(list1)
        return avr
    PREC_STD = avr([abs(float(i) - avr(lis1)) for i in lis1])
    return PREC_STD


def Prec_Of_Success(list1):
    
    """
    input: list in list of [area , 1 = found tree \ 0 = didnt found tree]
    list = [[93,1],[523,1],[223,0],[23,0]]
    Prec_Of_Success(list) = 71.4
    OutPut: prec of the Success
    """
    
    allarea    = sum([i[0] for i in list1])
    arror_area = sum([i[0] for i in list1 if i[1] == 0]) 
    a = (1 - (arror_area/allarea))*100
    return a

def Get_statistics(layer):
    
    list1 = []

    prec_uni_inter = [i.PRCT for i in arcpy.SearchCursor(layer) if i.PRCT != None]
    num_items_val  = len(prec_uni_inter)
    num_all_items  = len([i.PRCT for i in arcpy.SearchCursor(layer)])
    zeros = (num_all_items - num_all_items)
    prec_uni_inter = (prec_uni_inter + [0] * zeros)

    with arcpy.da.SearchCursor(layer,['SHAPE@AREA','PRCT']) as cursor:
        for row in cursor:
            if row[1] == None:
                list1.append([row[0],0])
            else:
                list1.append([row[0],1])
         
    STDer    = STDerror        (prec_uni_inter)
    Success  = Prec_Of_Success (list1)

    return STDer,Success
    

def Create_CSV(data,csv_name):
	try:
		df        = pd.DataFrame(data)
		df.to_csv(csv_name)
	except:
		print_arcpy_message("tool can't create excel file from pandas,working with CSV", status = 1)
				
		with open(csv_name,'w') as myfile:
			wr2 = csv.writer(myfile)
			for i in data:
				wr2.writerow([i])


def get_rasters_Multi_lists(folder):
        DSM = []
        DTM = []
        walk = arcpy.da.Walk (folder)
        for dirpath, dirnames, filenames in walk:
                for filename in filenames:
                        if filename.endswith('.tif'):
                                type1 = os.path.basename(os.path.dirname(dirpath))
                                if type1 == 'DSM':
                                        DSM.append(os.path.join (dirpath, filename))
                                elif type1 == 'DTM':
                                        DTM.append(os.path.join (dirpath, filename))
                                else:
                                        pass

        return DSM,DTM


def Get_data(feature_classes,filed_name,Trees_layer):

        outFile = r'in_memory\OutFile_'+filed_name
        arcpy.CreateFeatureclass_management (os.path.dirname (outFile), os.path.basename (outFile), "POLYGON")
        try:
                arcpy.AddField_management (outFile, filed_name, 'TEXT')
        except:
                pass

        point = arcpy.Point ()
        array = arcpy.Array ()
        corners = ["lowerLeft", "lowerRight", "upperRight", "upperLeft"]
        cursor = arcpy.InsertCursor (outFile)

        for Ras in feature_classes:

                feat = cursor.newRow ()
                r = arcpy.Raster (Ras)
                for corner in corners:
                        point.X = getattr (r.extent, "%s" % corner).X
                        point.Y = getattr (r.extent, "%s" % corner).Y
                        array.add (point)

                array.add (array.getObject (0))
                polygon    = arcpy.Polygon (array)
                feat.shape = polygon

                raster_name = os.path.realpath (Ras)
                feat.setValue (filed_name, str (raster_name))

                cursor.insertRow (feat)
                array.removeAll ()

        try:
                arcpy.AddField_management (Trees_layer, filed_name, "String", "", "", 500)
        except:
                pass

        Feature_layer = 'point_lyr_' + filed_name
        arcpy.MakeFeatureLayer_management (Trees_layer, Feature_layer)
        with arcpy.da.SearchCursor(outFile,['SHAPE@',filed_name]) as Scursor:
                for i in Scursor:
                        arcpy.SelectLayerByLocation_management (Feature_layer, "INTERSECT", i[0])
                        arcpy.CalculateField_management (Feature_layer, filed_name, "\"" + str (i[1]) + "\"", "VB")

def Remove_ras_files(raster):
        try:
                os.remove (raster)
                os.remove (raster + '.ovr')
                os.remove (raster + '.aux.xml')
                os.remove (raster + '.xml')
                os.remove (raster.split('.')[0] + '.tfw')
        except:
                pass


def Average(lst):
        return sum(lst) / len(lst)


def Exctract_NDSM(trees_layer):
        total_len_layer = int (str (arcpy.GetCount_management (trees_layer)))
        if total_len_layer > 0:
                folder = r'C:\\temp\try1'
                createFolder (folder)
                list1 = ['DSM', 'DTM', 'max', 'mean', 'min', 'OBJECTID']
                for i in list1:
                        add_field(trees_layer,i,'TEXT')

                list1.insert (0, 'SHAPE@')
                with arcpy.da.UpdateCursor (trees_layer, list1) as cursor:
                        for row in cursor:
                                if (str (row[1]) == 'None') or (str (row[2]) == 'None'):
                                        print_arcpy_message ("no raster Found", 1)
                                        pass
                                elif str(row[3]) != 'None':
                                        pass
                                        #print_arcpy_message ("Already got Value", 1)
                                        
                                else:
                                        # if str (type (row[0])) <> "<type 'NoneType'>":
                                        DSM = arcpy.Raster (row[1])
                                        DTM = arcpy.Raster (row[2])
                                        DSM_to_array = arcpy.RasterToNumPyArray (DSM, nodata_to_value=0)
                                        DTM_to_array = arcpy.RasterToNumPyArray  (DTM, nodata_to_value=0)
                                        outCon = (DSM_to_array - DTM_to_array)

                                        X          = getattr (DSM.extent, "lowerLeft").X
                                        Y          = getattr (DSM.extent, "lowerLeft").Y
                                        lower_left = arcpy.Point(X,Y)
                                        
                                        worked = False
                                        while worked == False:
                                                try:
                                                        New_ras = arcpy.NumPyArrayToRaster(outCon,lower_left,DSM.meanCellWidth,DSM.meanCellHeight)
                                                        worked = True
                                                except:
                                                        gc.collect()
                                                        print "Error, cleaning gc"

                                        geom = row[0]
                                        Raster = folder + '\\' + str (os.path.basename (row[1])) + '_' + str (row[-1]) + '_.tif'
                                        if arcpy.Exists (Raster):
                                                Remove_ras_files(Raster)

                                        arcpy.Clip_management (New_ras, "", Raster, geom, "127", "ClippingGeometry","NO_MAINTAIN_EXTENT")

                                        inRas = arcpy.Raster (Raster)
                                        arr = arcpy.RasterToNumPyArray (inRas, nodata_to_value=0)
                                        flat_list = [item for sublist in arr for item in sublist if item != 0]
                                        if flat_list:

                                                print_arcpy_message ('ID: {}, max: {}, Average: {}, min: {}'.format(str(row[-1]),str (max(flat_list)),str (Average(flat_list)),(min(flat_list))), status=1)

                                                row[3] = str (max(flat_list))
                                                row[4] = str (Average(flat_list))
                                                row[5] = str (min(flat_list))
                                                del arr
                                                del inRas
                                                cursor.updateRow (row)

                                        Remove_ras_files(Raster)
                                        del outCon
                                        del DSM_to_array
                                        del DTM_to_array
                                        del DSM
                                        del DTM
                                        gc.collect()
                                        

        else:
                print_arcpy_message ("no trees found to exctract mean", 1)


def Get_Ortho_data(folder,layer):

        total_len_layer = int(str(arcpy.GetCount_management(layer)))
        if total_len_layer > 0:
                
                outFile = r'in_memory\polyme2'
                if arcpy.arcpy.Exists(outFile):
                        pass
                else:
                        layer_poly = arcpy.CreateFeatureclass_management (os.path.dirname (outFile), os.path.basename (outFile), "POLYGON")

                feature_classes = []

                walk = arcpy.da.Walk (folder)
                for dirpath, dirnames, filenames in walk:
                        for filename in filenames:
                                if filename.endswith('.ecw'):
                                        feature_classes.append (os.path.join(dirpath, filename))


                try:
                        arcpy.AddField_management (outFile, "Rastername", "String", "", "", 500)
                except:
                        pass


                point = arcpy.Point ()
                array = arcpy.Array ()
                corners = ["lowerLeft", "lowerRight", "upperRight", "upperLeft"]
                cursor = arcpy.InsertCursor (outFile)

                for Ras in feature_classes:
                        Geometry     = []
                        feat = cursor.newRow ()
                        r = arcpy.Raster (Ras)
                        for corner in corners:
                                        point.X = getattr (r.extent, "%s" % corner).X
                                        point.Y = getattr (r.extent, "%s" % corner).Y
                                        array.add (point)
                                        
                        array.add (array.getObject (0))
                        polygon    = arcpy.Polygon (array)
                        feat.shape = polygon


                        raster_name = os.path.realpath(Ras)
                        feat.setValue ("Rastername", str(raster_name))

                        cursor.insertRow (feat)
                        array.removeAll ()

                del cursor  

                
                list_Upd = []
                try:
                        arcpy.AddField_management (layer, "Rastername", "String", "", "", 500)
                except:
                        pass
                arcpy.MakeFeatureLayer_management(layer,'point_lyr')
                Scursor = arcpy.SearchCursor(outFile)
                for i in Scursor:
                        arcpy.SelectLayerByLocation_management('point_lyr',"INTERSECT",i.shape)
                        arcpy.CalculateField_management('point_lyr','Rastername',"\""+str(i.Rastername)+"\"","VB")

        else:
                print_arcpy_message('Didnt Find items in layer Points',1)


def get_mean(points,Exists_Geom = ''):

        total_len_layer = int(str(arcpy.GetCount_management(points)))
        if total_len_layer > 0:
                if Exists_Geom == '':
                        print_arcpy_message("no input Exists_Geom",1)
                        pass
                else:
                        try:
                                arcpy.MakeFeatureLayer_management(points,"points_lyr")
                                arcpy.SelectLayerByLocation_management("points_lyr","INTERSECT",Exists_Geom)
                                arcpy.DeleteFeatures_management("points_lyr")
                        except:
                                print_arcpy_message("Coudent delete Exists Geom in fun: get_mean",1)
                                pass
                
                folder         = r'C:\\temp\try2'
                createFolder(folder)

                list1 = ['band1','band2','band3','band4',"Rastername","OBJECTID"]
                for i in list1:
                        add_field(points,i,"TEXT")

                raster_sample = [i.Rastername for i in arcpy.SearchCursor(points)][0]
                
                try:
                        existss = list(set([i.OBJECTID for i in arcpy.SearchCursor(points) if i.band3 != None]))
                except:
                        existss = []
                        pass
                

                list1.insert(0,"SHAPE@")
                num_finished    = 1
                num_exists      = len(existss)
                total_len = total_len_layer - num_exists
                with arcpy.da.UpdateCursor(points,list1) as cursor:
                        for row in cursor:
                                if str(row[5]) == 'None':
                                        print_arcpy_message("no raster Found",1)
                                        pass
                                elif row[6] in existss:
                                        print_arcpy_message("alreadt exists bands data",1)
                                        pass
                                else:
                                        if str(type(row[0])) <> "<type 'NoneType'>":
                                                geom = row[0]
                                                new_geom = geom.buffer(2)
                                                raster   = folder + '\\' + str(row[-1]) + '_.tif'
                                                if arcpy.Exists(raster):
                                                        pass
                                                else:    
                                                        arcpy.Clip_management     (row[5], "", raster,new_geom , "127", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
                                                inRas  = arcpy.Raster             (raster)
                                                arr    = arcpy.RasterToNumPyArray (inRas, nodata_to_value=0)
                                                row[1] = str(arr[0].mean())
                                                row[2] = str(arr[1].mean())
                                                row[3] = str(arr[2].mean())

                                                del arr
                                                del inRas
                                                
                                                Remove_ras_files(raster)

                                                cursor.updateRow(row)
                                                print_arcpy_message(str(num_finished) + '/' + str(total_len),1)
                                                num_finished += 1
                                                
                                                gc.collect()
        
        else:
                print_arcpy_message("no trees found to exctract mean",1)

def cacl_Tree_or_not(layer,red,green,blue):

        total_len_layer = int(str(arcpy.GetCount_management(layer)))
        if total_len_layer > 0:
                
                add_field(layer, "predict_1_0", "FLOAT")
                add_field(layer, "predict", "FLOAT")

                def yes_no(num):
                        if num > -165:
                                return 1
                        else:
                                return 0
                        

                def Green_leaf_index(red,green,blue):
                        # Vis Louhaichi et al. 2001

                        index = ((2*float(green)) - (float(red) - float(blue)))/((2*float(green)) + (float(red) + float(blue)))
                        return index
                        
                
                list_field = ["predict","predict_1_0","band1","band2","band3"]
                with arcpy.da.UpdateCursor(layer,list_field) as cursor:
                        for row in cursor:
                                if None not in [row[2],row[3],row[4]]:
                                        row[0] = Green_leaf_index(row[2],row[3],row[4])
                                        #row[1] = yes_no(row[0])
                                        cursor.updateRow(row)

        else:
                print_arcpy_message('No item in layer to calculate: Tree_or_not',1)


path        = r'F:\medad\Python_tools\ML_For_moshe\data\Pref_Unet_mosaic\Msk_mosaic.tif'
shp_orig    = r'\\netapp1\ChangeDetection\DEEP_TRAIN_SET\trees\RSH-1131_ITM_20cm_CNZ_19\shp.shp'

#  # # Constant Input # # #
fodler      = r'C:\\temp'
DEM_DTM_ras = r'\\netapp1\Rambo\2017_2018_Ortho_Final_Products\DTM_DSM\DTM_DSM_2017_2018_FINAL_PRODUCTS'
orth_folder = r'\\netapp1\Rambo\2017_2018_Ortho_Final_Products\OrthoMapi\Orthomapi_2017_2018_final_products\ITM\MEZUNZAR\50CM\ECW_50_AREA_A_B_D_F_G_2017_2018'
csv_name = fodler +'\\'+'Stats_' + str(datetime.datetime.now())[0:10]

# # # Raster to Shp and Analysis # # #

gdb               = create_Folder_GDB            (fodler)
predict_shp       = Raster_to_Shape              (path,gdb)
num               = Get_False_Type               (predict_shp,shp_orig)
FINISH            = Calc_Connection_Merge_Inter  (predict_shp,shp_orig,gdb = '')
del_field_list                                   (FINISH, ['gridcode','BUFF_DIST','ORIG_FID','TARGET_FID','ID_BLDG','AREA_BLDG'])
arcpy.Delete_management                          (predict_shp)

# #  # calc Statistics and export to csv # # #

STDer,Success = Get_statistics (FINISH)
data          = ["STDerror: "+str(STDer)] + ["Success rate: "+str(Success)]
Create_CSV      (data,csv_name)
print_arcpy_message("Total That have no match sample: {}".format(num))

#  #  # Get NDSM from ortho and calc min\mean\max # # #

DSM,DTM = get_rasters_Multi_lists  (DEM_DTM_ras)
Get_data        (DSM,"DSM",FINISH)
Get_data        (DTM,"DTM",FINISH)
Exctract_NDSM   (FINISH)

#  #  # Get RGB from ortho and calc green\red\blue #  #  #

Get_Ortho_data   (orth_folder,FINISH)
get_mean         (FINISH)
cacl_Tree_or_not (FINISH,"band1","band2","band3")


