import requests as r
import pandas as pd
from trading_client.atradingclient import ATradingClient

class LocalClient(ATradingClient):

    def __init__(self):
        super().__init__()

    def bar(self,tickers):
        self.market.connect()
        bars = self.market.query("prices",{"ticker":{"$in":tickers}})
        self.market.disconnect()
        return bars
    
    def orders(self):
        self.db.connect()
        data = self.db.retrieve("orders")
        self.db.disconnect()
        return data
    
    def reset_account(self):
        self.db.connect()
        self.db.drop("account")
        self.db.drop("positions")
        self.db.store("account",pd.DataFrame([{
                        "cash": 100000,
                        "portfolio_value": 100000
                        }]))
        self.db.disconnect()
    
    def account(self):
        self.db.connect()
        data = self.db.retrieve("account")
        self.db.disconnect()
        return data
    
    def update_account(self,account):
        self.db.connect()
        self.db.drop("account")
        self.db.store("account",pd.DataFrame([account]))
        self.db.disconnect()
    
    def update_positions(self,order):
        self.db.connect()
        self.db.store("positions",pd.DataFrame([order]))
        self.db.disconnect()
        
    def positions(self):
        self.db.connect()
        data = self.db.retrieve("positions")
        self.db.disconnect()
        return data
    
    def buy(self,ticker,adjclose,amount):
        parameters = {
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
            "symbol": ticker,
            "notional": amount,
            "adjclose":adjclose,
            "quantity":float(amount/adjclose)
            }
        return parameters
    
    def sell(self,ticker,adjclose,amount):
        url = "https://api.alpaca.markets/v2/orders"
        parameters = {
            "side": "sell",
            "type": "market",
            "time_in_force": "day",
            "symbol": ticker,
            "notional": amount,
            "adjclose":adjclose
            }
        return parameters
    
    def close(self):
        params = {}
        url = "https://api.alpaca.markets/v2/positions?cancel_orders=true"
        return url