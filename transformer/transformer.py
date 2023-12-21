from processor.processor import Processor as processor
from database.adatabase import ADatabase
from tqdm import tqdm
import pandas as pd

class Transformer(object):

    @classmethod
    def transform(self,strategy):
        market = ADatabase("market")
        market.connect()
        sp500 = market.retrieve("sp500")
        market.disconnect()
        tickers = sp500["ticker"].values
        market = ADatabase("market")
        market.connect()
        prices = []
        for ticker in tickers[::50]:
            try:
                ticker_prices = processor.column_date_processing(market.query("prices",{"ticker":ticker}))
                ticker_prices.sort_values("date",inplace=True)
                simulation = strategy.signal(ticker_prices)
                prices.append(simulation.dropna())
            except Exception as e:
                print(ticker,str(e))
                continue
        market.disconnect()
        return pd.concat(prices)
