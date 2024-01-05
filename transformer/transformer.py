from processor.processor import Processor as processor
from database.adatabase import ADatabase
from returns.returns import Returns
import pandas as pd
from tqdm import tqdm
from extractor.alp_extractor import ALPExtractor

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
        overhead = strategy.overhead()
        for ticker in tickers:
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
    
    @classmethod
    def cloud_transform(self,strategy,start,end):
        russell1000 = pd.read_html("https://en.wikipedia.org/wiki/Russell_1000_Index")[2].rename(columns={"Ticker":"ticker"})
        tickers = russell1000["ticker"].values
        prices = []
        overhead = strategy.overhead()
        for ticker in tqdm(tickers):
            try:
                included_columns = ["date","buy_date","sell_date","week","weekday","ticker","adjclose","signal","buy_price","sell_price","return"]
                ticker_prices = processor.column_date_processing(ALPExtractor.prices(ticker,start,end))
                ticker_prices["ticker"] = ticker
                ticker_prices.sort_values("date",inplace=True)
                ticker_prices = strategy.signal(overhead,ticker_prices)
                ticker_prices = Returns.returns(strategy,ticker_prices)
                prices.append(ticker_prices[included_columns].iloc[100:])
            except Exception as e:
                print(str(e))
                continue
        return pd.concat(prices)
