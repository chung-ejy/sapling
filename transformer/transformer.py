from processor.processor import Processor as processor
from database.adatabase import ADatabase
from returns.returns import Returns
import pandas as pd
from tqdm import tqdm
from extractor.alp_extractor import ALPExtractor
<<<<<<< HEAD
from extractor.pandas_extractor import PandasExtractor
=======

>>>>>>> 24978f5cd672cfa053b59580225eb82420f685fb
class Transformer(object):

    @classmethod
    def transform(self,strategy):
        market = ADatabase("market")
        market.cloud_connect()
        prices = []
        overhead = strategy.overhead()
        for ticker in strategy.tickers:
            try:
                ticker_prices = processor.column_date_processing(market.query("prices",{"ticker":ticker}))
                ticker_prices.sort_values("date",inplace=True)
                ticker_prices = strategy.signal(overhead,ticker_prices)
                ticker_prices = Returns.returns(strategy,ticker_prices)
                prices.append(ticker_prices)
            except Exception as e:
                print(str(e))
                continue
        market.disconnect()
        return pd.concat(prices)
    
    @classmethod
    def cloud_transform(self,strategy,start,end):
        prices = []
        overhead = strategy.overhead()
        for ticker in tqdm(strategy.tickers):
            try:
                ticker_prices = processor.column_date_processing(ALPExtractor.prices(ticker,start,end))
                ticker_prices["ticker"] = ticker
                ticker_prices.sort_values("date",inplace=True)
                ticker_prices = strategy.signal(overhead,ticker_prices)
                ticker_prices = Returns.returns(strategy,ticker_prices)
                prices.append(ticker_prices)
            except Exception as e:
                print(str(e))
                continue
        return pd.concat(prices)
<<<<<<< HEAD

    @classmethod
    def kospi_transform(self,strategy,start,end):
        prices = []
        overhead = strategy.overhead()
        for ticker in tqdm(strategy.tickers):
            try:
                ticker_prices = PandasExtractor.prices(ticker,start,end)
                ticker_prices["adjclose"] = ticker_prices["Close"]
                ticker_prices["date"] = ticker_prices["Date"]
                ticker_prices["ticker"] = ticker
                ticker_prices.sort_values("date",inplace=True)
                ticker_prices = ticker_prices.reset_index(drop=True)
                ticker_prices = processor.column_date_processing(ticker_prices[["date","ticker","adjclose"]])
                ticker_prices["adjclose"] = [float(x) for x in ticker_prices["adjclose"]]
                ticker_prices = strategy.signal(overhead,ticker_prices)
                ticker_prices = Returns.returns(strategy,ticker_prices)
                prices.append(ticker_prices.reset_index())
            except Exception as e:
                print(str(e))
                continue
        return pd.concat(prices)
=======
>>>>>>> 24978f5cd672cfa053b59580225eb82420f685fb
