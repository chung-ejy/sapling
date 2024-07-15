import os
import requests as r
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
secret = os.getenv("")
key = os.getenv("")

class ATradingClient(object):

    def __init__(self):
        self.headers = {
            'APCA-API-KEY-ID': key,
            'APCA-API-SECRET-KEY': secret,
            'accept': 'application/json'
        }
        
    def orders(self):
        return ""
    
    def bar(self,tickers):
        return ""
    
    def account(self):
        return ""
    
    def positions(self):
        return ""
    
    def buy(self,ticker,price,amount):
        return ""
    
    def sell(self,ticker,price,amount):
        return ""
    
    def close(self):
        return ""