import requests as r
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("APCAKEY")
secret = os.getenv("APCASECRET")
import pandas as pd

class ALPExtractor(object):

    @classmethod
    def prices(self,ticker,start,end):
        headers = {
            'APCA-API-KEY-ID': key,
            'APCA-API-SECRET-KEY': secret,
            'accept': 'application/json'
        }
        params = {
            "symbols":ticker,
            "adjustment":"raw",
            "timeframe":"1Day",
            "feed":"sip",
            "sort":"asc",
            "start":start.strftime("%Y-%m-%d"),
            "end":end.strftime("%Y-%m-%d")
        }
        url = "https://data.alpaca.markets/v2/stocks/bars"
        requestBody = r.get(url,params=params,headers=headers)
        data =  pd.DataFrame(requestBody.json()["bars"][ticker]).rename(columns={"c":"adjclose","t":"date"})[["date","adjclose"]]
        data["ticker"] = ticker
        return data
    
    @classmethod
    def account(self):
        headers = {
            'APCA-API-KEY-ID': key,
            'APCA-API-SECRET-KEY': secret,
            'accept': 'application/json'
        }
        params = {}
        url = "https://paper-api.alpaca.markets/v2/account"
        requestBody = r.get(url,params=params,headers=headers)
        return requestBody.json()

    @classmethod
    def buy(self,ticker,qty):
        headers = {
            "APCA-API-KEY-ID":key,
            "APCA-API-SECRET-ID":secret,
            "accept":"application/json"
        }
        data = {
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
            "symbol": ticker,
            "qty": qty
            }
        url = "https://paper-api.alpaca.markets/v2/orders"
        requestBody = r.post(url,data=data,headers=headers)
    
    @classmethod
    def sell(self,ticker,qty):
        headers = {
            "APCA-API-KEY-ID":key,
            "APCA-API-SECRET-ID":secret,
            "accept":"application/json"
        }
        data = {
            "side": "sell",
            "type": "market",
            "time_in_force": "day",
            "symbol": ticker,
            "qty": qty
            }
        url = "https://paper-api.alpaca.markets/v2/orders"
        requestBody = r.post(url,data=data,headers=headers)
    
    @classmethod
    def close(self):
        headers = {
            "APCA-API-KEY-ID":key,
            "APCA-API-SECRET-ID":secret,
            "accept":"application/json"
        }
        params = {}
        url = "https://paper-api.alpaca.markets/v2/positions"
        requestBody = r.delete(url,params=params,headers=headers)