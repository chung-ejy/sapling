from database.adatabase import ADatabase
from strategy.astrategy import AStrategy
import pandas as  pd
from processor.processor import Processor as processor
from tqdm import tqdm
import numpy as np
import warnings
warnings.simplefilter(action="ignore")

class OptimalQuarterly(AStrategy):
    
    def __init__(self):
        super().__init__("optimal_quarterly")
        self.metric = "expected_return"
        self.growth = False

    def sell_clause(self,date,stock):
        return (date.quarter != stock.buy_date.quarter)
    
    def load_dataset(self):
        sp500 = self.load_sp500()
        market_yield, spy = self.load_macro()
        prices = []
        self.market.connect()
        for ticker in tqdm(sp500["ticker"].unique()):
            try:
                price = processor.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                price.sort_values("date",inplace=True)
                price["prediction"] = price["adjclose"].shift(-90)
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