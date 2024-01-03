from pymongo import MongoClient, DESCENDING
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("MONGOKEY")
import certifi
ca = certifi.where()

class ADatabase(object):
    
    def __init__(self,name):
        self.name = name
        super().__init__()
    
    def connect(self):
        self.client = MongoClient("localhost",27017)
    
    def cloud_connect(self):
        self.client = MongoClient(token,tlsCAFile=ca)
    
    def disconnect(self):
        self.client.close()

    def store(self,table_name,data):
        try:
            db = self.client[self.name]
            table = db[table_name]
            records = data.to_dict("records")
            table.insert_many(records)
        except Exception as e:
            print(self.name,table_name,str(e))
    
    def retrieve(self,table_name):
        try:
            db = self.client[self.name]
            table = db[table_name]
            data = table.find({},{"_id":0},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,table_name,str(e))
    
    def query(self,table_name,query):
        try:
            db = self.client[self.name]
            table = db[table_name]
            data = table.find(query,{"_id":0},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,table_name,str(e))
    
    def create_index(self,table_name,col):
        try:
            db = self.client[self.name]
            table = db[table_name]
            table.create_index([(col, DESCENDING)], unique=False)
        except Exception as e:
            print(self.name,table_name,str(e))
    
    def drop(self,table_name):
        try:
            db = self.client[self.name]
            table = db[table_name]
            table.drop()
        except Exception as e:
            print(self.name,table_name,str(e))
    