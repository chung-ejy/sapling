from database.adatabase import ADatabase
from strategy.astrategy import AStrategy
import pandas as  pd
from processor.processor import Processor as processor
import pandas_datareader.data as web
import pandas_datareader as pdr
from tqdm import tqdm
import numpy as np
import warnings
warnings.simplefilter(action="ignore")

class FamaFrenchQuarterly(AStrategy):
    
    def __init__(self):
        super().__init__("fama_french_quarterly")
        self.metric = "excess_return"
        self.growth = False

    def sell_clause(self,date,stock):
        return (date.quarter != stock.buy_date.quarter)
    
    def load_dataset(self):
        sp500 = self.load_sp500()
        market_yield, spy = self.load_macro()
        fama_french_factors = web.DataReader('F-F_Research_Data_Factors_daily',"famafrench")[0]
        fff = fama_french_factors.reset_index().rename(columns={"Date":"date"})
        fff["date"] = [str(x) for x in fff["date"]]
        fff = processor.column_date_processing(fff)
        self.factors = [x for x in fff.columns if x not in  ["date","rf"]]
        prices = []
        self.market.connect()
        for ticker in tqdm(sp500["ticker"].unique()):
            try:
                price = processor.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                price.sort_values("date",inplace=True)
                price = price.merge(fff,on="date",how="left")
                price["prediction"] = price["adjclose"].shift(60)
                price["risk"] = price["adjclose"].rolling(100).std()
                for factor in self.factors:
                    price["factor_return"] = price[factor].rolling(100).mean()
                    price["beta"] = price["prediction"].rolling(100).cov(price["factor_return"])
                    price["var"] = price["factor_return"].rolling(100).var()
                    price[f"{factor}_prediction"] = price["beta"] * (price["prediction"])
                price["prediction"] = [sum([row[1][f"{factor}_prediction"] for x in self.factors])/len(self.factors) for row in price.iterrows()]
                price = price[["date","ticker","adjclose","prediction"]]
                price = self.index_factor_load(price,sp500,spy,market_yield)
                prices.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        self.market.disconnect()
        sim = pd.concat(prices)
        self.save_sim(sim)
    
    def get_sim(self):
        self.db.connect()
        sim = processor.column_date_processing(self.db.retrieve("sim")).sort_values("date")
        self.db.disconnect()
        return sim