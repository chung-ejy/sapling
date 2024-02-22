import requests as r
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

class ALPPaperExtractor(object):
    
    def __init__(self):
        self.key =os.getenv("APCAPAPERKEY")
        self.secret = os.getenv("APCAPAPERSECRET")

    def prices(self,ticker,start,end):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            'accept': 'application/json'
        }
        params = {
            "symbols":ticker,
            "adjustment":"split",
            "timeframe":"1Day",
            "feed":"sip",
            "sort":"asc",
            "start":start.strftime("%Y-%m-%d"),
        }
        url = "https://data.alpaca.markets/v2/stocks/bars"
        requestBody = r.get(url,params=params,headers=headers)
        data =  pd.DataFrame(requestBody.json()["bars"][ticker]).rename(columns={"c":"adjclose","t":"date"})[["date","adjclose"]]
        data["ticker"] = ticker
        return data
    
    def crypto_prices(self,ticker,start,end):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            'accept': 'application/json'
        }
        params = {
            "symbols":ticker,
            "timeframe":"15min",
            "sort":"asc",
            "start":start.strftime("%Y-%m-%d")
        }
        url = "https://data.alpaca.markets/v1beta3/crypto/us/bars"
        requestBody = r.get(url,params=params,headers=headers)
        data =  pd.DataFrame(requestBody.json()["bars"][ticker]).rename(columns={"c":"adjclose","t":"date"})[["date","adjclose"]]
        data["ticker"] = ticker
        return data
    
    def account(self):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            'accept': 'application/json'
        }
        params = {}
        url = "https://api.paper-alpaca.markets/v2/account"
        requestBody = r.get(url,params=params,headers=headers)
        return requestBody.json()

    def buy(self,ticker,notional):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            "accept": "application/json",
            "content-type": "application/json"
        }
        data = {
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
            "symbol": ticker,
            "notional": notional
            }
        url = "https://api.alpaca.markets/v2/orders"
        requestBody = r.post(url,json=data,headers=headers)
        return requestBody.json()
    
    def close(self):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            "accept":"application/json"
        }
        params = {}
        url = "https://api.paper-alpaca.markets/v2/positions?cancel_orders=true"
        requestBody = r.delete(url,params=params,headers=headers)