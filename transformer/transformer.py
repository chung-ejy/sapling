from processor.processor import Processor as processor
from database.adatabase import ADatabase
from returns.returns import Returns
import pandas as pd
class Transformer(object):

    @classmethod
    def transform(self,strategy):
        market = ADatabase("market")
        market.connect()
        russell1000 = market.retrieve("russell1000")
        market.disconnect()
        tickers = russell1000["ticker"].values
        market.connect()
        prices = []
        for ticker in tickers:
            try:
                included_columns = ["date","buy_date","sell_date","week","weekday","ticker","adjclose","signal","buy_price","sell_price","return"]
                ticker_prices = processor.column_date_processing(market.query("prices",{"ticker":ticker}))
                ticker_prices.sort_values("date",inplace=True)
                simulation = strategy.signal(ticker_prices)
                simulation = Returns.returns(strategy,ticker_prices)
                prices.append(simulation[included_columns].iloc[100:])
            except Exception as e:
                print(str(e))
                continue
        market.disconnect()
        return pd.concat(prices)
