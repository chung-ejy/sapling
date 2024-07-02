import pandas as pd
from trading_client.atradingclient import ATradingClient
from parameters.AParameters import AParameters
from time import sleep

class LiveTrader(object):

    def __init__(self,trading_client: ATradingClient,parameters: AParameters):
        self.trading_client = trading_client
        self.parameters = parameters
    
    def trade(self,recommendations: pd.DataFrame):
        recommendations.sort_values("expected_return",ascending=False,inplace=True)
        account = self.trading_client.account()
        orders = self.trading_client.orders()
        cash = float(account["cash"])
        pv = float(account["portfolio_value"])
        positions = self.trading_client.positions()
        sectors = list(recommendations["GICS Sector"].unique())
        sectors.sort()
        notional = float(pv/self.parameters.number_of_positions)
        if positions.index.size < self.parameters.number_of_positions:
            for i in range(self.parameters.number_of_positions):
                try:
                    sector = sectors[i] 
                    recommendation = recommendations[recommendations["GICS Sector"]==sector].iloc[0]
                    recommendation_order = pd.DataFrame([]) if orders.index.size < 1 else orders[orders["symbol"]==recommendation["ticker"]] 
                    position =  pd.DataFrame([]) if positions.index.size < 1 else positions[positions["symbol"]==recommendation["ticker"]] 
                    if cash > 1 and cash >= notional and recommendation_order.index.size < 1 and position.index.size < 1:
                        ticker = recommendation["ticker"]
                        price = round(recommendation["adjclose"],2)
                        amount = max(1,int(notional/price))
                        self.trading_client.buy(ticker,price,amount)  
                        account = self.trading_client.account()
                        cash = float(account["cash"]) 
                    else:
                         continue
                except Exception as e:
                     print(str(e))
        else:
            positions = positions.rename(columns={"symbol":"ticker"}).merge(recommendations[["ticker","GICS Sector","expected_return"]],on="ticker",how="left")
            try:
                sector = sectors[i] 
                recommendation = recommendations[recommendations["GICS Sector"]==sector].iloc[0]
                recommendation_order = pd.DataFrame([]) if orders.index.size < 1 else orders[orders["symbol"]==recommendation["ticker"]] 
                position = positions[positions["GICS Sector"]==sector]
                price = round(float(position["current_price"]),2)
                amount = int(position["qty"])
                ticker = position["ticker"]
                if ticker != recommendation["ticker"] and position["expected_return"] <= 0:
                    self.trading_client.sell(ticker,price,amount)
                    sleep(5)
                    orders = self.trading_client.orders()
                    orders = orders[orders["symbol"]==ticker]
                    account = self.trading_client.account()
                    cash = float(account["cash"])
                    while orders.index.size > 0:
                        orders = self.trading_client.orders()
                        orders = orders[orders["symbol"]==ticker]
                        account = self.trading_client.account()
                        cash = float(account["cash"])
                        sleep(5)
                    ticker = recommendation["ticker"]
                    price = round(recommendation["adjclose"],2)
                    amount = max(1,int(notional/price))
                    self.trading_client.buy(ticker,price,amount)
            except Exception as e:
                print(str(e))
            sleep(1)
                