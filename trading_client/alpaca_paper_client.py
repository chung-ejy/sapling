import os
import requests as r
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
secret = os.getenv("APCAPAPERSECRET")
key = os.getenv("APCAPAPERKEY")

class AlpacaPaperClient(object):

    def __init__(self):
        self.headers = {
            'APCA-API-KEY-ID': key,
            'APCA-API-SECRET-KEY': secret,
            'accept': 'application/json'
        }
    
    def bar(self,tickers):
        url = "https://data.alpaca.markets/v2/stocks/bars/latest"
        data = {
            "symbols":",".join(tickers)
        }
        columns=["adjclose","high","low","trades","open","date","volume","volume_weighted"]
        response = r.get(url,params=data,headers=self.headers).json()
        df = pd.DataFrame(response["bars"].values())
        for i in range(len(df.columns)):
            df.rename(columns={list(df.columns)[i]:columns[i]},inplace=True)
        df["ticker"] = response["bars"].keys()
        return df
    
    def account(self):
        url = "https://paper-api.alpaca.markets/v2/account"
        response = r.get(url,headers=self.headers).json()
        return response
    
    def positions(self):
        url = "https://paper-api.alpaca.markets/v2/positions"
        response = r.get(url,headers=self.headers).json()
        return pd.DataFrame(response)
    
    def buy(self,ticker,price,amount):
        url = "https://paper-api.alpaca.markets/v2/orders"
        parameters = {
            "side": "buy",
            "type": "limit",
            "time_in_force": "gtc",
            "symbol": ticker,
            "limit_price": price,
            "qty": amount
            }
        response = r.post(url,json=parameters,headers=self.headers)
        return response.json()
    
    def sell(self,ticker,price,amount):
        url = "https://paper-api.alpaca.markets/v2/orders"
        parameters = {
            "side": "sell",
            "type": "limit",
            "time_in_force": "gtc",
            "symbol": ticker,
            "limit_price": price,
            "qty": amount
            }
        response = r.post(url,json=parameters,headers=self.headers)
        return response.json()