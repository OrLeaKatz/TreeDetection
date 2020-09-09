import json
import sqlite3




class Read_Geo_json():
    
    def __init__(self,json_file_path):
        # Build DB in memory 
        conn = sqlite3.connect(":memory:")
        c    = conn.cursor()
        c.execute('''CREATE table DB_polygons (KEY text, geometry real)''')
        
        # build data strcuters
        self.jsonfile  = json_file_path
        self.c         = c
        self.Dictonery = {}
        self.List_Data = []

    
    def Get_Json_to_Sqlite(self):
        # extract ID and Geometry from json to sqlite3 DB
        with open(self.jsonfile) as f:
            json_data = json.load(f)
            for feature in json_data["features"]:
                self.c.execute('''insert into DB_polygons (KEY,geometry) values ("{}","{}")'''.format(feature["id"],feature["geometry"]["coordinates"]))
        
            f.close()
        
        return self.c
    
    def Json_To_dictonery(self):
        # extract ID and Geometry from json to dictonery
        with open(self.jsonfile) as f:
            json_data = json.load(f)
            for feature in json_data["features"]:
                self.Dictonery[feature["id"]] = feature["geometry"]["coordinates"]
            f.close()
        
        return self.Dictonery
                
    def Json_to_list(self):
         with open(self.jsonfile) as f:
            json_data = json.load(f)
            for feature in json_data["features"]:
                self.List_Data.append([feature["id"],feature["geometry"]["coordinates"]])
                
         return self.List_Data
        
    def ShowData(self):
        
        self.c = self.Get_Json_to_Sqlite()
        self.c.execute("SELECT * FROM DB_polygons")
        
        rows = self.c.fetchall()
        
        for row in rows:
            print(row)

json_file_path = r"E:\DEV\JSON_2_SQLITE\polygon2.json"


my_json1 = Read_Geo_json(json_file_path)
dict1 = my_json1.Json_to_list()
