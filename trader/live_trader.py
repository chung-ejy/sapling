import pandas as pd
from trading_client.alpaca_paper_client import AlpacaPaperClient
from parameters.AParameters import AParameters
class LiveTrader(object):

    def __init__(self,trading_client: AlpacaPaperClient,parameters: AParameters):
        self.trading_client = trading_client
        self.parameters = parameters
    
    def trade(self,recommendations: pd.DataFrame):
        recommendations.sort_values("expected_return",ascending=False)
        account = self.trading_client.account()
        cash = float(account["cash"])
        pv = float(account["portfolio_value"])
        positions = self.trading_client.positions()
        sectors = list(recommendations["GICS Sector"].unique())
        sectors.sort()
        for i in range(self.parameters.number_of_positions):
            try:
                sector = sectors[i] 
                recommendation = recommendations[recommendations["GICS Sector"]==sector].iloc[0]
                position = positions.iloc[i] if positions.index.size > 0 else {}
                notional = float(pv/self.parameters.number_of_positions)
                if position == {} and cash > 1 and cash >= notional:
                    ticker = recommendation["ticker"]
                    price = round(recommendation["adjclose"],2)
                    amount = int(notional/price)
                    self.trading_client.buy(ticker,price,amount)
                elif position != {}:
                    ticker = position["symbol"]
                    price = round(position["current_price"],2)
                    amount = position["qty"]
                    position_data = recommendations[recommendations["ticker"]==position["symbol"]]
                    if True < 0:
                        self.trading_client.sell(ticker,price,amount)
                    else:
                        continue
                else:
                    continue
            except Exception as e:
                str(e)
                