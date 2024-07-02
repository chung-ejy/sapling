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
        cash = float(account["cash"])
        pv = float(account["portfolio_value"])
        positions = self.trading_client.positions()
        if positions.index.size > 0:
            positions = positions.rename(columns={"symbol":"ticker"}).merge(
            recommendations[["ticker","GICS Sector","expected_return"]],on="ticker",how="left"
            )
        sectors = list(recommendations["GICS Sector"].unique())
        sectors.sort()
        for i in range(self.parameters.number_of_positions):
            try:
                sector = sectors[i] 
                recommendation = recommendations[recommendations["GICS Sector"]==sector].iloc[0]
                position = positions[positions["GICS Sector"]==sector].iloc[0] if positions.index.size > 0 else {}
                notional = float(pv/self.parameters.number_of_positions)
                if position == {} and cash > 1 and cash >= notional:
                    ticker = recommendation["ticker"]
                    price = round(recommendation["adjclose"],2)
                    amount = int(notional/price)
                    self.trading_client.buy(ticker,price,amount)
                elif position != {}:
                    price = round(position["current_price"],2)
                    amount = position["qty"]
                    ticker = position["ticker"]
                    if True:
                        self.trading_client.sell(ticker,price,amount)
                        orders = self.trading_client.orders()
                        while orders.index.size > 0:
                            orders = self.trading_client.orders()
                            sleep(1)
                        notional = price * amount
                        ticker = recommendation["ticker"]
                        price = round(recommendation["adjclose"],2)
                        amount = int(notional/price)
                        self.trading_client.buy(ticker,price,amount)
                    else:
                        continue
                else:
                    continue
            except Exception as e:
                str(e)
                