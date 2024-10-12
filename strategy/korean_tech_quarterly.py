from database.adatabase import ADatabase
from strategy.astrategy import AStrategy
import pandas as  pd
from processor.processor import Processor as processor
from tqdm import tqdm
import numpy as np
import warnings
from xgboost import XGBRegressor

warnings.simplefilter(action="ignore")

class KoreanTechQuarterly(AStrategy):
    
    def __init__(self):
        super().__init__("korean_tech_quarterly") 
        self.metric = "expected_return"
        self.growth = True

    def sell_clause(self,date,stock):
        return date.quarter != stock.buy_date.quarter
    
    def load_dataset(self):

        kospi = pd.read_csv("kospi.csv").rename(columns={"Issue code":"ticker"})
        market_yield, spy = self.load_macro()
        
        factors = [str(x) for x in kospi["ticker"][:7]]
        self.market.connect()
        self.db.connect()
        factors_df = []
        for ticker in tqdm(factors):
            try:
                price = processor.column_date_processing(self.market.query("kr_prices",{"ticker":str(ticker)}).rename(columns={"Date":"date"}))
                price["adjclose"] = [int(x) for x in price["close"]]
                factors_df.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        self.market.disconnect()
        self.db.disconnect()
        factors_df = pd.concat(factors_df).pivot_table(index="date",columns="ticker",values="adjclose")
        
        prices = []
        self.market.connect()
        self.db.connect()
        for ticker in tqdm(kospi["ticker"].unique()):
            try:
                price = processor.column_date_processing(self.market.query("kr_prices",{"ticker":str(ticker)}).rename(columns={"Date":"date"}))
                if price.index.size > 0:
                    price["adjclose"] = [int(x) for x in price["close"]]
                    price.sort_values("date",inplace=True)
                    price = price.merge(factors_df.reset_index(),on="date",how="left")
                    price["y"] = price["adjclose"].rolling(90).mean().shift(-90)
                    training_data = price[:int(price.index.size/2)].dropna()
                    model = XGBRegressor()
                    model.fit(training_data[factors],training_data["y"])
                    price["prediction"] = model.predict(price[factors])
                    price = price.iloc[100:]
                    price = price.merge(spy[["date","spy"]],on="date",how="left")
                    price = price.merge(market_yield[["date","rf"]],on="date",how="left")
                    price = self.index_factor_load(price)
                    prices.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        self.market.disconnect()
        self.db.disconnect()
        self.market.disconnect()

        sim = pd.concat(prices)
        self.save_sim(sim)
    
    def get_sim(self):
        self.db.connect()
        sim = processor.column_date_processing(self.db.retrieve("sim")).sort_values("date")
        self.db.disconnect()
        return sim