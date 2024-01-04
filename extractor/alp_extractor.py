import requests as r
import os
from dotenv import load_dotenv
load_dotenv()
paperkey = os.getenv("APCAPAPERKEY")
papersecret = os.getenv("APCAPAPERSECRET")
import pandas as pd

class ALPExtractor(object):

    @classmethod
    def prices(self,ticker,start,end):
        headers = {
            'APCA-API-KEY-ID': paperkey,
            'APCA-API-SECRET-KEY': papersecret,
            'accept': 'application/json'
        }
        params = {
            "symbols":ticker,
            "adjustment":"split",
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
            'APCA-API-KEY-ID': paperkey,
            'APCA-API-SECRET-KEY': papersecret,
            'accept': 'application/json'
        }
        params = {}
        url = "https://paper-api.alpaca.markets/v2/account"
        requestBody = r.get(url,params=params,headers=headers)
        return requestBody.json()

    @classmethod
    def buy(self,ticker,qty):
        headers = {
            "APCA-API-KEY-ID":paperkey,
            "APCA-API-SECRET-KEY":papersecret,
            "accept": "application/json",
            "content-type": "application/json"
        }
        data = {
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
            "symbol": ticker,
            "qty": qty
            }
        url = "https://paper-api.alpaca.markets/v2/orders"
        requestBody = r.post(url,json=data,headers=headers)
        return requestBody
    
    @classmethod
    def buy_stop_loss(self,ticker,adjclose,qty):
        headers = {
            "APCA-API-KEY-ID":paperkey,
            "APCA-API-SECRET-KEY":papersecret,
            "accept": "application/json",
            "content-type": "application/json"
        }
        data = {
            "side": "buy",
            "symbol": ticker,
            "type": "market",
            "qty": qty,
            "time_in_force": "gtc",
            "order_class": "oto",
            "stop_loss": {
                "stop_price": round(adjclose * 0.95,2),
                "limit_price": round(adjclose * 0.94,2)
            }
        }
        url = "https://paper-api.alpaca.markets/v2/orders"
        requestBody = r.post(url,json=data,headers=headers)
        return requestBody
    
    @classmethod
    def close(self):
        headers = {
            "APCA-API-KEY-ID":paperkey,
            "APCA-API-SECRET-KEY":papersecret,
            "accept":"application/json"
        }
        params = {}
        url = "https://paper-api.alpaca.markets/v2/positions?cancel_orders=true"
        requestBody = r.delete(url,params=params,headers=headers)