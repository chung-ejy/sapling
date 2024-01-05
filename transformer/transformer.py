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
        prices = []
        overhead = strategy.overhead()
        for ticker in strategy.tickers:
            try:
                included_columns = ["date","buy_date","sell_date","week","weekday","ticker","adjclose","signal","buy_price","sell_price","return"]
                ticker_prices = processor.column_date_processing(market.query("prices",{"ticker":ticker}))
                ticker_prices.sort_values("date",inplace=True)
                ticker_prices = strategy.signal(overhead,ticker_prices)
                ticker_prices = Returns.returns(strategy,ticker_prices)
                prices.append(ticker_prices[included_columns])
            except Exception as e:
                continue
        market.disconnect()
        return pd.concat(prices)
    