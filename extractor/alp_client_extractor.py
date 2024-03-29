import requests as r
import pandas as pd

class ALPClientExtractor(object):
    
    def __init__(self,key,secret):
        self.key = key
        self.secret = secret
            
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
    
    def account(self):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            'accept': 'application/json'
        }
        params = {}
        url = "https://api.alpaca.markets/v2/account"
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
    
    def sell(self,ticker,notional):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            "accept": "application/json",
            "content-type": "application/json"
        }
        data = {
            "side": "sell",
            "type": "market",
            "time_in_force": "day",
            "symbol": ticker,
            "notional": notional
            }
        url = "https://api.alpaca.markets/v2/orders"
        requestBody = r.post(url,json=data,headers=headers)
        return requestBody.json()
    
    def buy_stop_loss(self,ticker,adjclose,notional):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            "accept": "application/json",
            "content-type": "application/json"
        }
        data = {
            "side": "buy",
            "symbol": ticker,
            "type": "market",
            "notional": notional,
            "time_in_force": "day",
            "order_class": "oto",
            "stop_loss": {
                "stop_price": round(adjclose * 0.95,2),
                "limit_price": round(adjclose * 0.94,2)
            }
        }
        url = "https://api.alpaca.markets/v2/orders"
        requestBody = r.post(url,json=data,headers=headers)
        return requestBody
    
    def close(self):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            "accept":"application/json"
        }
        params = {}
        url = "https://api.alpaca.markets/v2/positions?cancel_orders=true"
        requestBody = r.delete(url,params=params,headers=headers)