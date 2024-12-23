from strategy.astrategy import AStrategy
import pandas as  pd
import warnings
from asset.exposure import Exposure
from tqdm import tqdm

warnings.simplefilter(action="ignore")

class COEVWeekly(AStrategy):
    
    def __init__(self):
        super().__init__("coev_weekly","sp500")
        self.growth = False

    def sell_clause(self,stock,market_data):
        return market_data.date.weekday() == 4
    
    def factor_load(self,standard_df):
        prices = []
        for ticker in tqdm(self.tickers):
            try:
                price = standard_df[standard_df["ticker"]==ticker].sort_values("date")
                price.sort_values("date",inplace=True)
                price["factor"] = price["adjclose"].rolling(100).std() / price["adjclose"].rolling(100).mean()
                if price.index.size > 0:
                    prices.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        sim = pd.concat(prices).dropna()
        return sim
    
    def signal(self,sim:pd.DataFrame):
        sim["rank"] = sim.groupby("date",group_keys=False)["factor"].apply(pd.qcut,q=10,labels=False,duplicates="drop")
        sim["exposure"] = [Exposure.LONG if x > 8 else Exposure.SHORT if x < 1 else Exposure.NONE for x in sim["rank"]]
        return sim.drop("rank",axis=1)