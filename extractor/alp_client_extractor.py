import requests as r
import pandas as pd
from datetime import datetime
class ALPClientExtractor(object):
    
    def __init__(self,key,secret):
        self.key = key
        self.secret = secret
    
    def clock(self):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            'accept': 'application/json'
        }
        url = "https://paper-api.alpaca.markets/v2/clock"
        requestBody = r.get(url,headers=headers)
        return requestBody.json()
    
    def crypto_interval(self,ticker,start):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            'accept': 'application/json'
        }
        params = {
            "symbols":ticker,
            "timeframe":"1Min",
            "sort":"asc",
            "limit":str(10000),
            "start":start.strftime("%Y-%m-%d")
        }
        url = "https://data.alpaca.markets/v1beta3/crypto/us/bars"
        requestBody = r.get(url,params=params,headers=headers)
        return requestBody.json()
    
    def crypto(self,ticker,start,end):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            'accept': 'application/json'
        }
        params = {
            "symbols":ticker,
            "timeframe":"1day",
            "sort":"asc",
            "limit":str(10000),
            "start":start.strftime("%Y-%m-%d"),
            # "end":end.strftime("%Y-%m-%d")
        }
        url = "https://data.alpaca.markets/v1beta3/crypto/us/bars"
        requestBody = r.get(url,params=params,headers=headers)
        data =  pd.DataFrame(requestBody.json()["bars"][ticker]).rename(columns={"c":"adjclose","t":"date"})[["date","adjclose"]]
        data["ticker"] = ticker
        return data
    
    def prices(self,ticker,start,end):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            'accept': 'application/json'
        }
        params = {
            "symbols":ticker,
            "adjustment":"all",
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
    
    def prices_bulk(self,ticker,start,end):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            'accept': 'application/json'
        }
        params = {
            "symbols":ticker,
            "adjustment":"all",
            "timeframe":"1Day",
            "feed":"sip",
            "sort":"asc",
            "limit":10000,
            "start":start.strftime("%Y-%m-%d"),
        }
        url = "https://data.alpaca.markets/v2/stocks/bars"
        requestBody = r.get(url,params=params,headers=headers)
        return requestBody.json()

    def prices_minute(self,ticker,start,end):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            'accept': 'application/json'
        }
        params = {
            "symbols":ticker,
            "adjustment":"all",
            "timeframe":"1min",
            "feed":"sip",
            "sort":"asc",
        }
        url = "https://data.alpaca.markets/v2/stocks/bars"
        requestBody = r.get(url,params=params,headers=headers)
        data =  pd.DataFrame(requestBody.json()["bars"][ticker]).rename(columns={"c":"adjclose","t":"date","v":"volume"})[["date","adjclose","volume"]]
        data["ticker"] = ticker
        return data
    
    def parse_option_symbol(self,option_symbol):
        # Ticker symbol is the first characters (AAPL)
        ticker = option_symbol[:4]
        
        # Expiration date is the next characters (241018)
        expiration_date = datetime.strptime(option_symbol[4:10],"%y%m%d")
        
        # Option type is the next character (P for Put, C for Call)
        option_type = option_symbol[10]
        
        # Strike price is the remaining characters (00110000)
        strike_price = float(option_symbol[11:]) / 1000  # Convert to decimal
        
        return option_symbol, ticker, expiration_date, option_type, strike_price

    def option_chains(self,ticker):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            'accept': 'application/json'
        }
        params = {
            "feed":"indicative",
        }
        url = f"https://data.alpaca.markets/v1beta1/options/snapshots/{ticker}"
        requestBody = r.get(url,params=params,headers=headers)
        stuff = [self.parse_option_symbol(x) for x in requestBody.json()["snapshots"].keys()]
        return pd.DataFrame(stuff,columns=["symbol","ticker","expiration_date","option_type","strike_price"])
    
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

    def crypto_buy(self,ticker,notional):
        headers = {
            'APCA-API-KEY-ID': self.key,
            'APCA-API-SECRET-KEY': self.secret,
            "accept": "application/json",
            "content-type": "application/json"
        }
        data = {
            "side": "buy",
            "type": "market",
            "time_in_force": "gtc",
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