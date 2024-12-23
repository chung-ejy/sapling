from strategy.astrategy import AStrategy
import pandas as  pd
import warnings
from asset.exposure import Exposure
from tqdm import tqdm
from equations.capm import CAPM
warnings.simplefilter(action="ignore")

class RollingAverageWeekly(AStrategy):
    
    def __init__(self):
        super().__init__("rolling_average_weekly","sp500")
        self.metric = "excess_return"
        self.growth = False

    def sell_clause(self,stock,market_data):
        return market_data.date.weekday() == 4
    
    def factor_load(self,standard_df):
        prices = []
        for ticker in tqdm(self.tickers):
            try:
                price = standard_df[standard_df["ticker"]==ticker].sort_values("date")
                price.sort_values("date",inplace=True)
                price["prediction"] = price["adjclose"].rolling(100).mean()
                prices.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        sim = pd.concat(prices)
        sim = CAPM.apply(sim)
        return sim
    
    def signal(self,sim:pd.DataFrame):
        sim["rank"] = sim.groupby("date",group_keys=False)["factor"].apply(pd.qcut,q=10,labels=False,duplicates="drop")
        sim["exposure"] = [Exposure.LONG if x > 8 else Exposure.SHORT if x < 1 else Exposure.NONE for x in sim["rank"]]
        return sim.drop("rank",axis=1)