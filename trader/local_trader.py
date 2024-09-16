import pandas as pd
from metric.ametric import AMetric
from trading_client.atradingclient import ATradingClient
from time import sleep
from processor.processor import Processor
from datetime import timedelta
class LocalTrader(object):

    def __init__(self, metric: AMetric,trading_client: ATradingClient):
        self.trading_client = trading_client
        self.metric = metric
    
    def preprocessing(self,tickers):
        chunks = [list(tickers[i:i + 25]) for i in range(0, len(tickers), 25)]
        prices = []
        for chunk in chunks:
            bars = Processor.column_date_processing(self.trading_client.bar(chunk)).sort_values("date")
            # metric calculation
            for ticker in bars["ticker"].unique():
                price = bars[bars["ticker"]==ticker]
                price = self.metric.create_metric(price)
                prices.append(price)
        prices = pd.concat(prices).sort_values("date")
        return prices
    
    def trade(self,account,positions,date,recommendations):
        todays_recs = recommendations[recommendations["date"]==date]
        if todays_recs.index.size >= self.metric.positions:
            todays_recs.sort_values(self.metric.name,ascending=self.metric.ascending,inplace=True)
            ## updates
            new_positions = []
            if len(positions) == self.metric.positions:
                account["portfolio_value"] = 0
                for i in range(self.metric.positions):
                    position = positions[i].copy()
                    ticker = position["symbol"]
                    position["adjclose"] = todays_recs[todays_recs["ticker"]==ticker]["adjclose"].item()
                    position["date"] = date
                    new_positions.append(position)
                    account["portfolio_value"] += position["adjclose"] * position["quantity"]
            if date.weekday() == 0:
                new_positions = []  
                pv = float(account["portfolio_value"])
                notional = round(float(pv/self.metric.positions),2)    
                for i in range(self.metric.positions):
                    recommendation = todays_recs.iloc[i]
                    ticker = recommendation["ticker"]
                    adjclose = recommendation["adjclose"]
                    order = self.trading_client.buy(ticker,adjclose,notional)
                    order["buy_date"] = date
                    order["buy_price"] = adjclose
                    order["date"] = date
                    order["position"] = i
                    order["name"] = self.metric.name
                    order["positions"] = self.metric.positions
                    order["boolean"] = self.metric.ascending
                    new_positions.append(order)
                return account, new_positions
            else:
                return account, new_positions
                

                