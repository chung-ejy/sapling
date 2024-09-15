import os
import requests as r
import pandas as pd
from dotenv import load_dotenv
from database.adatabase import ADatabase
from metric.ametric import AMetric
load_dotenv()
secret = os.getenv("")
key = os.getenv("")

class ATradingClient(object):

    def __init__(self):
        self.market = ADatabase("market")
        self.db = ADatabase("sapling")
        
    def bar(self,tickers):
        self.market.connect()
        bars = self.market.query("prices",{"ticker":{"$in":tickers}})
        self.market.disconnect()
        return bars
            
    def orders(self):
        return ""
    
    def account(self):
        return ""
    
    def update_account(self):
        return ""
    
    def positions(self):
        return ""
    
    def buy(self,ticker,price,amount):
        return ""
    
    def sell(self,ticker,price,amount):
        return ""
    
    def close(self):
        return ""