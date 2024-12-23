from strategy.anaistrategy import AnAIStrategy
import pandas as  pd
from processor.processor import Processor as processor
from tqdm import tqdm
import warnings
warnings.simplefilter(action="ignore")
from asset.exposure import Exposure
from asset.stock import Stock
from equations.capm import CAPM


class MagnificentSevenQuarterly(AnAIStrategy):
    
    def __init__(self):
        super().__init__("magnificent_seven_quarterly","sp500",["AMZN","NVDA","AAPL","META","GOOGL","TSLA","MSFT"])
        self.metric = "excess_return"
        self.growth = False
        self.start_year = 2013
        self.end_year = 2020

    def sell_clause(self,stock,market_data):
        current_quarter = (market_data.date.month - 1) // 3 + 1
        purchase_quarter = (stock.purchase_date.month - 1) // 3 + 1
        return (current_quarter != purchase_quarter)
    
    def factor_load(self,standard_df):
        prices = []
        self.market.connect()
        factors_df = self.load_factors()
        self.market.disconnect()
        for ticker in self.tickers:
            try:
                price = standard_df[standard_df["ticker"]==ticker].sort_values("date")
                price.sort_values("date",inplace=True)
                price["year"] = [x.year for x in price["date"]]
                price = price.merge(factors_df.reset_index(),on="date",how="left")
                price["y"] = price["adjclose"].rolling(60).mean().shift(-60)
                training_data = price[(price["year"]>=self.start_year) & (price["year"]<self.end_year)].dropna()
                price = self.model(training_data,price)
                price = price[(price["year"]>=self.end_year-1)].reset_index(drop=True)
                if price.index.size > 0:
                    prices.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        sim = pd.concat(prices).reset_index(drop=True)
        sim = CAPM.apply(sim)
        return sim
    
    def signal(self,sim:pd.DataFrame):
        sim["rank"] = sim.groupby("date",group_keys=False)["factor"].rank(method="dense", ascending=False).astype(int)
        sim["exposure"] = [Exposure.LONG if x < 10 else Exposure.SHORT if x > 490 else Exposure.NONE for x in sim["rank"]]
        return sim.drop("rank",axis=1)
    

    def load_factors(self):
        factors_df = []
        for ticker in tqdm(self.factors):
            try:
                price = processor.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                factors_df.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        factors_df = pd.concat(factors_df).pivot_table(index="date",columns="ticker",values="adjclose")
        return factors_df