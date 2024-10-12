from database.adatabase import ADatabase
import pandas as  pd
from processor.processor import Processor as processor
from tqdm import tqdm
import numpy as np
import warnings
warnings.simplefilter(action="ignore")

class CoefficientOfVariance(object):
    
    def __init__(self):
        self.name = "coefficient_of_variance"
        self.db = ADatabase(self.name)
        self.market = ADatabase("market")
        self.metric = "coefficient_of_variance"


    def sell_clause(self,date,stock):
        return stock.ticker != "" and (date-stock.buy_date).days > 6
    
    def load_dataset(self):

        russell1000 = pd.read_html("https://en.wikipedia.org/wiki/Russell_1000_Index")[2].rename(columns={"Symbol":"ticker"})

        prices = []
        self.market.connect()
        for ticker in tqdm(russell1000["ticker"].unique()):
            try:
                price = processor.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                price.sort_values("date",inplace=True)
                price = price.merge(russell1000[["ticker","GICS Sector"]],on="ticker",how="left")
                price[self.metric] = price["adjclose"].rolling(100).std() / price["adjclose"].rolling(100).mean()
                prices.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
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