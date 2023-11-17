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
    
    # @classmethod
    # def prices(self,ticker):
    #     headers = {
    #         "APCA-API-KEY-ID":key,
    #         "APCA-API-SECRET-ID":secret,
    #         "accept":"application/json"
    #     }
    #     params = {
    #         "symbols":ticker,
    #         "adjustment":"split",
    #         "feed":"sip",
    #         "sort":"asc",
    #     }
    #     url = "https://data.alpaca.markets/v2/stocks/bars"
    #     requestBody = r.get(url,params=params,headers=headers)
    #     return requestBody.json()

    #     @classmethod
    # def prices(self,ticker):
    #     headers = {
    #         "APCA-API-KEY-ID":key,
    #         "APCA-API-SECRET-ID":secret,
    #         "accept":"application/json"
    #     }
    #     params = {
    #         "symbols":ticker,
    #         "adjustment":"split",
    #         "feed":"sip",
    #         "sort":"asc",
    #     }
    #     url = "https://data.alpaca.markets/v2/stocks/bars"
    #     requestBody = r.get(url,params=params,headers=headers)
    #     return requestBody.json()
    
    #     @classmethod
    # def prices(self,ticker):
    #     headers = {
    #         "APCA-API-KEY-ID":key,
    #         "APCA-API-SECRET-ID":secret,
    #         "accept":"application/json"
    #     }
    #     params = {
    #         "symbols":ticker,
    #         "adjustment":"split",
    #         "feed":"sip",
    #         "sort":"asc",
    #     }
    #     url = "https://data.alpaca.markets/v2/stocks/bars"
    #     requestBody = r.get(url,params=params,headers=headers)
    #     return requestBody.json()
    
    #     @classmethod
    # def prices(self,ticker):
    #     headers = {
    #         "APCA-API-KEY-ID":key,
    #         "APCA-API-SECRET-ID":secret,
    #         "accept":"application/json"
    #     }
    #     params = {
    #         "symbols":ticker,
    #         "adjustment":"split",
    #         "feed":"sip",
    #         "sort":"asc",
    #     }
    #     url = "https://data.alpaca.markets/v2/stocks/bars"
    #     requestBody = r.get(url,params=params,headers=headers)
    #     return requestBody.json()
    
    #     @classmethod
    # def prices(self,ticker):
    #     headers = {
    #         "APCA-API-KEY-ID":key,
    #         "APCA-API-SECRET-ID":secret,
    #         "accept":"application/json"
    #     }
    #     params = {
    #         "symbols":ticker,
    #         "adjustment":"split",
    #         "feed":"sip",
    #         "sort":"asc",
    #     }
    #     url = "https://data.alpaca.markets/v2/stocks/bars"
    #     requestBody = r.get(url,params=params,headers=headers)
    #     return requestBody.json()