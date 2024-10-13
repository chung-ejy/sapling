from database.adatabase import ADatabase
from processor.processor import Processor as processor
import numpy as np
class AStrategy(object):

    def __init__(self,name):
        self.name = name
        self.db = ADatabase(self.name)
        self.market = ADatabase("market")
        self.sec = ADatabase("sec")
        self.fred = ADatabase("fred")
    

    def load_sp500(self):
        self.market.connect()
        sp500 = self.market.retrieve("sp500")
        self.market.disconnect()
        return sp500
    
    def load_macro(self):
        self.fred.connect()
        market_yield = self.fred.retrieve("market_yield")
        market_yield = market_yield.rename(columns={"value":"rf"})
        market_yield["rf"] = market_yield["rf"].replace(".",np.nan)
        market_yield.dropna(inplace=True)
        market_yield["rf"] = [float(x)/100 for x in market_yield["rf"]]
        market_yield["date"] = market_yield["date"].shift(-5)
        market_yield = processor.column_date_processing(market_yield)
        spy = self.fred.retrieve("sp500")
        spy = spy.rename(columns={"value":"spy"})
        spy["spy"] = spy["spy"].replace(".",np.nan)
        spy.dropna(inplace=True)
        spy["spy"] = [float(x) for x in spy["spy"]]
        spy["date"] = spy["date"].shift(-5)
        spy = processor.column_date_processing(spy)
        self.fred.disconnect()
        return market_yield, spy

    def index_factor_load(self,price,constituents,spy,market_yield):
        price = price.merge(constituents[["ticker","GICS Sector"]],on="ticker",how="left")
        price = price.merge(spy[["date","spy"]],on="date",how="left")
        price = price.merge(market_yield[["date","rf"]],on="date",how="left")
        price["expected_return"] = (price["prediction"] - price["adjclose"]) / price["adjclose"]
        price["historical_return"] = price["adjclose"].pct_change(90)
        price["factor_return"] = price["spy"].pct_change(90)
        price["cov"] = price["factor_return"].rolling(100).cov(price["expected_return"])
        price["market_cov"] = price["cov"].abs()
        price["var"] = price["factor_return"].rolling(100).var()
        price["beta"] = price["cov"] / price["var"]
        price["excess_return"] = price["rf"] + price["beta"] * (price["expected_return"] - price["rf"])
        return price

    def save_sim(self,sim):
        sim = sim[["date","ticker","adjclose","market_cov","GICS Sector",self.metric]]
        self.db.connect()
        self.db.drop("sim")
        self.db.store("sim",sim)
        self.db.disconnect()
    