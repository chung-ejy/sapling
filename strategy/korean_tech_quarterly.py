from database.adatabase import ADatabase
from strategy.anaistrategy import AnAIStrategy
import pandas as  pd
from processor.processor import Processor as processor
from tqdm import tqdm
import numpy as np
import warnings
import math
warnings.simplefilter(action="ignore")

class KoreanTechQuarterly(AnAIStrategy):
    
    def __init__(self):
        super().__init__("korean_tech_quarterly",["5930","660","373220","207940","5380"]) 
        self.metric = "excess_return"
        self.growth = False
        self.start_year = 2013
        self.end_year = 2020
        self.sim_end_year = 2025
    
    def sell_clause(self,date,stock):
        return date.quarter != stock.buy_date.quarter
    
    def load_factors(self):
        self.market.connect()
        self.db.connect()
        factors_df = []
        for ticker in tqdm(self.factors):
            try:
                price = processor.column_date_processing(self.market.query("kr_prices",{"ticker":str(ticker)}).rename(columns={"Date":"date"}))
                price["adjclose"] = [int(x) for x in price["close"]]
                factors_df.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        self.market.disconnect()
        self.db.disconnect()
        factors_df = pd.concat(factors_df).pivot_table(index="date",columns="ticker",values="adjclose").reset_index()
        return factors_df
    
    def load_dataset(self):
        kospi = pd.read_csv("kospi.csv").rename(columns={"Issue code":"ticker"})
        kospi["ticker"] = [str(x) for x in kospi["ticker"]]
        kospi["GICS Sector"] = [round(math.log10(x)) for x in kospi["Total market cap."]]
        market_yield, spy = self.load_macro()
        factors_df = self.load_factors()
        prices = []
        self.market.connect()
        for ticker in tqdm(kospi["ticker"].unique()):
            try:
                price = processor.column_date_processing(self.market.query("kr_prices",{"ticker":str(ticker)}).rename(columns={"Date":"date"}))
                if price.index.size > 0:
                    price["adjclose"] = [int(x) for x in price["close"]]
                    price.sort_values("date",inplace=True)
                    price["year"] = [x.year for x in price["date"]]
                    price = price.merge(factors_df.reset_index(),on="date",how="left")
                    price["y"] = price["adjclose"].rolling(60).mean().shift(-60)
                    training_data = price[(price["year"]>=self.start_year) & (price["year"]<self.end_year)].dropna()
                    price = self.model(training_data,price)
                    price = price[(price["year"]>=self.end_year-1)]
                    price = self.index_factor_load(price,kospi,spy,market_yield)
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