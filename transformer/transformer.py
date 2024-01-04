from processor.processor import Processor as processor
from database.adatabase import ADatabase
from returns.returns import Returns
import pandas as pd
from tqdm import tqdm

class Transformer(object):

    @classmethod
    def transform(self,strategy):
        market = ADatabase("market")
        market.cloud_connect()
        sp100 = market.retrieve("sp100")
        market.disconnect()
        tickers = sp100["ticker"].values
        market.cloud_connect()
        prices = []
        for ticker in tickers:
            try:
                ticker_prices = processor.column_date_processing(market.query("prices",{"ticker":ticker}))[["date","week","weekday","ticker","adjclose"]]
                ticker_prices.sort_values("date",inplace=True)
                simulation = strategy.signal(ticker_prices)
                simulation = Returns.returns(strategy,ticker_prices)
                prices.append(simulation.iloc[100:])
            except Exception as e:
                continue
        market.disconnect()
        return pd.concat(prices)
