from strategy.anaistrategy import AnAIStrategy
import pandas as  pd
from processor.processor import Processor as processor
from tqdm import tqdm
import warnings

warnings.simplefilter(action="ignore")

class MagnificentSevenQuarterly(AnAIStrategy):
    
    def __init__(self):
        super().__init__("magnificent_seven_quarterly",["AMZN","NVDA","AAPL","META","GOOGL","TSLA","MSFT"])
        self.metric = "expected_return"
        self.growth = False
        self.start_year = 2013
        self.end_year = 2020
        self.sim_end_year = 2025
        
    def sell_clause(self,date,stock):
        return date.quarter != stock.buy_date.quarter
    

    def load_factors(self):
        factors_df = []
        for ticker in tqdm(self.factors):
            try:
                price = processor.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                factors_df.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        self.market.disconnect()
        self.db.disconnect()
        factors_df = pd.concat(factors_df).pivot_table(index="date",columns="ticker",values="adjclose")
        return factors_df
    
    def load_dataset(self):

        sp500 = self.load_sp500()
        market_yield, spy = self.load_macro()
        self.market.connect()
        self.db.connect()
        factors_df = self.load_factors()

        prices = []
        self.market.connect()
        self.db.connect()
        for ticker in tqdm(sp500["ticker"].unique()):
            try:
                price = processor.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                price.sort_values("date",inplace=True)
                price["year"] = [x.year for x in price["date"]]
                price = price.merge(factors_df.reset_index(),on="date",how="left")
                price["y"] = price["adjclose"].rolling(90).mean().shift(-90)
                training_data = price[(price["year"]>=self.start_year) & (price["year"]<self.end_year)].dropna()
                price = self.model(training_data,price)
                price = price[(price["year"]>=self.end_year-1)]
                price = self.index_factor_load(price,sp500,spy,market_yield)
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