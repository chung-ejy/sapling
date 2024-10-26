from database.adatabase import ADatabase
from strategy.astrategy import AStrategy
import pandas as  pd
from processor.processor import Processor as processor
from tqdm import tqdm
import numpy as np
import warnings
warnings.simplefilter(action="ignore")

class JPSingleIndexQuarterly(AStrategy):
    
    def __init__(self):
        super().__init__("jp_single_index_quarterly")
        self.metric = "excess_return"
        self.growth = False
        self.jp_quant = ADatabase("jp_quant")

    def sell_clause(self,date,stock):
        return (date.quarter != stock.buy_date.quarter)
    
    def load_dataset(self):
        self.jp_quant.connect()
        core500 = self.jp_quant.retrieve("core500").rename(columns={"size":"GICS Sector"})
        core500["ticker"] = [str(x) for x in core500["ticker"]]
        self.jp_quant.disconnect()
        market_yield, spy = self.load_macro()

        prices = []
        self.jp_quant.connect()
        for ticker in tqdm(list(core500["ticker"].unique())):
            try:
                price = processor.column_date_processing(self.jp_quant.query("prices",{"ticker":str(ticker)}))
                price.sort_values("date",inplace=True)
                price["adjclose"] = [float(x) / 100 for x in price["adjclose"]]
                price["prediction"] = price["adjclose"].shift(60)
                price = self.index_factor_load(price,core500,spy,market_yield)
                prices.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        self.jp_quant.disconnect()
        sim = pd.concat(prices)
        self.save_sim(sim)
    
    def get_sim(self):
        self.db.connect()
        sim = processor.column_date_processing(self.db.retrieve("sim")).sort_values("date")
        self.db.disconnect()
        return sim