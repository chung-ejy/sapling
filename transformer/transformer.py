from processor.processor import Processor as processor
from database.adatabase import ADatabase
from returns.returns import Returns
import pandas as pd
from extractor.alp_extractor import ALPExtractor
from tqdm import tqdm
class Transformer(object):
    
    @classmethod
    def transform(self,strategy,start,end):
        prices = []
        overhead = strategy.overhead()
        for ticker in strategy.tickers:
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
    
    @classmethod
    def local_transform(self,strategy,start,end):
        market = ADatabase("market")
        prices = []
        overhead = strategy.overhead()
        market.connect()
        for ticker in strategy.tickers:
            try:
                ticker_prices = processor.column_date_processing(market.query(strategy.prices,{"ticker":ticker}))
                ticker_prices["ticker"] = ticker
                ticker_prices.sort_values("date",inplace=True)
                ticker_prices = strategy.signal(overhead,ticker_prices)
                ticker_prices = Returns.returns(strategy,ticker_prices)
                prices.append(ticker_prices)
            except Exception as e:
                print(str(e))
                continue
        market.disconnect()
        return pd.concat(prices)
