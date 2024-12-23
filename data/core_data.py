from database.adatabase import ADatabase
from processor.processor import Processor as processor
import numpy as np
import pandas as pd
from tqdm import tqdm

class CoreData(object):
    
    def __init__(self):
        self.market = ADatabase("market")
        self.fred = ADatabase("fred")
    
    def load_index(self):
        self.market.connect()
        self.index = self.market.retrieve("sp500")
        self.market.disconnect()
        self.tickers = list(self.index["ticker"].unique())

    def macro_dataframe(self):
        self.fred.connect()
        market_yield = self.fred.retrieve("market_yield")
        market_yield = market_yield.rename(columns={"value":"rf"})
        market_yield["rf"] = market_yield["rf"].replace(".",np.nan)
        market_yield.dropna(inplace=True)
        market_yield["rf"] = [float(x)/100 for x in market_yield["rf"]]
        market_yield = processor.column_date_processing(market_yield)
        spy = self.fred.retrieve("sp500_projections").rename(columns={"prediction":"sp500_prediction"})
        spy = processor.column_date_processing(spy)
        self.fred.disconnect()
        return market_yield[["date","rf"]].merge(spy,on="date",how="left")
    
    def core_dataframe(self):
        prices = []
        macro = self.macro_dataframe()
        self.market.connect()
        for ticker in tqdm(self.tickers):
            try:
                price = processor.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                price.sort_values("date",inplace=True)
                prices.append(price[["date","ticker","adjclose"]])
            except Exception as e:
                print(ticker,str(e))
                continue
        self.market.disconnect()
        sim = pd.concat(prices).merge(macro,on="date",how="left")
        return sim.dropna()
    
