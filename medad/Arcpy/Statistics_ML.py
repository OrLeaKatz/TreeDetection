import arcpy
import pandas as pd
import csv

prec_uni_inter = [99,23,45,67,45,0]
Area           = [[93,1],[523,1],[223,0],[23,0]]


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

def STDerror(lis1):
    
    # input: list of intersect over union prec
    #list = [99,23,45,67,45]
    #STDerror(list) = 24.3
    # OutPut: STDerror of intersect over union prec 
    
    def avr(list1):
        avr = sum(list1)/len(list1)
        return avr
    
    PREC_STD = avr([abs(float(i) - avr(lis1)) for i in lis1])
    return PREC_STD


def Prec_Of_Success(list1):
    
    # input: list in list of [area , 1 = found tree, 0 = didnt found tree]
    #list = [[93,1],[523,1],[223,0],[23,0]]
    #Prec_Of_Success(list) = 71.4
    # OutPut: prec of the Success
    
    allarea    = sum([i[0] for i in list1])
    arror_area = sum([i[0] for i in list1 if i[1] == 0]) 
    a = (1 - (arror_area/allarea))*100
    return a

def Get_statistics(layer):
    
    list1 = []
    prec_uni_inter = [i.PRCT for i in arcpy.SearchCursor(layer)]
    with arcpy.da.SearchCursor(layer,['SHAPE@AREA','PRCT']) as cursor:
        for row in cursor():
            if row[1] == None:
                list1.append([row[0],0])
            else:
                list1.append([row[0],1])
         
    STDer    = STDerror        (list1)
    Success  = Prec_Of_Success (prec_uni_inter)
    
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
                
       
         
STDer,Success = Get_statistics (layer)
data          = ["STDerror: "+str(STDer)] + ["Success rate: "+str(Success)]
Create_CSV     (data,csv_name)



