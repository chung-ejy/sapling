import pandas as pd
from metric.ametric import AMetric
from trading_client.atradingclient import ATradingClient
from time import sleep
from processor.processor import Processor


class LiveTrader(object):

    def __init__(self, metric: AMetric,trading_client: ATradingClient):
        self.trading_client = trading_client
        self.metric = metric
    
    def preprocessing(self,tickers):
        chunks = [list(tickers[i:i + 25]) for i in range(0, len(tickers), 25)]
        prices = []
        for chunk in chunks:
            bars = Processor.column_date_processing(self.trading_client.bar(chunk)).sort_values("date")
            for ticker in bars["ticker"].unique():
                price = bars[bars["ticker"]==ticker]
                price = self.metric.create_metric(price)
                prices.append(price)
        prices = pd.concat(prices).sort_values("date")
        return prices
    
    def trade(self,account,positions,date,recommendations):
        todays_recs = recommendations[recommendations["date"]==recommendations["date"].max()]
        if todays_recs.index.size >= self.metric.positions:
            todays_recs.sort_values(self.metric.name,ascending=self.metric.ascending,inplace=True)
            pv = float(account["portfolio_value"])
            notional = round(float(pv/self.metric.positions),2)
            if positions.index.size == self.metric.positions:
                if date.weekday() == 4:
                    self.trading_client.close()
            elif positions.index.size == 0:    
                for i in range(self.metric.positions):
                    recommendation = todays_recs.iloc[i]
                    ticker = recommendation["ticker"]
                    adjclose = recommendation["adjclose"]
                    self.trading_client.buy(ticker,adjclose,notional)
            else:
                return

                