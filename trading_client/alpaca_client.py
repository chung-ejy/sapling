import os
import requests as r
import pandas as pd
from dotenv import load_dotenv
from trading_client.atradingclient import ATradingClient
load_dotenv()

class AlpacaClient(ATradingClient):

    def __init__(self):
        super().__init__()
        self.headers = {
            'APCA-API-KEY-ID': os.getenv("APCAKEY"),
            'APCA-API-SECRET-KEY': os.getenv("APCASECRET"),
            'accept': 'application/json'
        }

    def orders(self):
        url = "https://api.alpaca.markets/v2/orders"
        response = r.get(url,headers=self.headers).json()
        return pd.DataFrame(response)
    
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
        url = "https://api.alpaca.markets/v2/account"
        response = r.get(url,headers=self.headers).json()
        return response
    
    def positions(self):
        url = "https://api.alpaca.markets/v2/positions"
        response = r.get(url,headers=self.headers).json()
        return pd.DataFrame(response)
    
    def buy(self,ticker,adjclose,amount):
        url = "https://api.alpaca.markets/v2/orders"
        parameters = {
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
            "symbol": ticker,
            "notional": amount
            }
        response = r.post(url,json=parameters,headers=self.headers)
        return response.json()
    
    def crypto_buy(self,ticker,notional):
        data = {
            "side": "buy",
            "type": "market",
            "time_in_force": "gtc",
            "symbol": ticker,
            "notional": notional
            }
        url = "https://api.alpaca.markets/v2/orders"
        requestBody = r.post(url,json=data,headers=self.headers)
        return requestBody.json()
    
    def sell(self,ticker,amount):
        url = "https://api.alpaca.markets/v2/orders"
        parameters = {
            "side": "sell",
            "type": "market",
            "time_in_force": "day",
            "symbol": ticker,
            "notional": amount
            }
        response = r.post(url,json=parameters,headers=self.headers)
        return response.json()
    
    def close(self):
        params = {}
        url = "https://api.alpaca.markets/v2/positions?cancel_orders=true"
        requestBody = r.delete(url,params=params,headers=self.headers)
        return requestBody.json()