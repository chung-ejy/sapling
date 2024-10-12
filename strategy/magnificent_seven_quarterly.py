from database.adatabase import ADatabase
import pandas as  pd
from processor.processor import Processor as processor
from tqdm import tqdm
import numpy as np
import warnings
from xgboost import XGBRegressor

warnings.simplefilter(action="ignore")

class MagnificentSevenQuarterly(object):
    
    def __init__(self):
        self.name = "magnificent_seven_quarterly"
        self.db = ADatabase(self.name)
        self.market = ADatabase("market")
        self.fred = ADatabase("fred")
        self.metric = "excess_return"

    def sell_clause(self,date,stock):
        return date.quarter != stock.buy_date.quarter
    
    def load_dataset(self):

        russell1000 = pd.read_html("https://en.wikipedia.org/wiki/Russell_1000_Index")[2].rename(columns={"Symbol":"ticker"})
        self.fred.connect()
        market_yield = self.fred.retrieve("market_yield")
        market_yield = market_yield.rename(columns={"value":"rf"})
        market_yield["rf"] = market_yield["rf"].replace(".",np.nan)
        market_yield.dropna(inplace=True)
        market_yield["rf"] = [float(x)/100 for x in market_yield["rf"]]
        market_yield = processor.column_date_processing(market_yield)
        spy = self.fred.retrieve("sp500")
        spy = spy.rename(columns={"value":"spy"})
        spy["spy"] = spy["spy"].replace(".",np.nan)
        spy.dropna(inplace=True)
        spy["spy"] = [float(x) for x in spy["spy"]]
        spy = processor.column_date_processing(spy)
        spy = spy.sort_values("date")
        self.fred.disconnect()
        
        factors = ["AMZN","NVDA","AAPL","META","GOOGL","TSLA","MSFT"]
        self.market.connect()
        self.db.connect()
        factors_df = []
        for ticker in tqdm(factors):
            try:
                price = processor.column_date_processing(self.market.query("prices",{"ticker":ticker}))
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
        for ticker in tqdm(russell1000["ticker"].unique()):
            try:
                price = processor.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                price.sort_values("date",inplace=True)
                price = price.merge(factors_df.reset_index(),on="date",how="left")
                price["y"] = price["adjclose"].rolling(90).mean().shift(-90)
                training_data = price[:int(price.index.size/2)].dropna()
                model = XGBRegressor()
                model.fit(training_data[factors],training_data["y"])
                price["prediction"] = model.predict(price[factors])
                price = price.merge(spy[["date","spy"]],on="date",how="left")
                price = price.merge(market_yield[["date","rf"]],on="date",how="left")
                price = price.merge(russell1000[["ticker","GICS Sub-Industry"]],on="ticker",how="left")
                price["expected_return"] = (price["prediction"] - price["adjclose"]) / price["adjclose"]
                price["historical_return"] = price["adjclose"].pct_change(90)
                price["factor_return"] = price["spy"].pct_change(90)
                price["cov"] = price["factor_return"].rolling(100).cov(price["expected_return"])
                price["var"] = price["factor_return"].rolling(100).var()
                price["beta"] = price["cov"] / price["var"]
                price["excess_return"] = price["rf"] + price["beta"] * (price["expected_return"] - price["rf"])
                prices.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        self.market.disconnect()
        self.db.disconnect()
        self.market.disconnect()
        sim = pd.concat(prices)
        
        sim = sim[["date","ticker","adjclose",self.metric]].dropna()
        self.db.connect()
        self.db.drop("sim")
        self.db.store("sim",sim)
        self.db.disconnect()
    
    def get_sim(self):
        self.db.connect()
        sim = processor.column_date_processing(self.db.retrieve("sim")).sort_values("date")
        self.db.disconnect()
        return sim