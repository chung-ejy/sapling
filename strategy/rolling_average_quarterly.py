from strategy.astrategy import AStrategy
import pandas as  pd
import warnings
from asset.exposure import Exposure
from equations.capm import CAPM
warnings.simplefilter(action="ignore")

class RollingAverageQuarterly(AStrategy):
    
    def __init__(self):
        super().__init__("rolling_average_quarterly","sp500")
        self.growth = False

    def sell_clause(self,stock,market_data):
        current_quarter = (market_data.date.month - 1) // 3 + 1
        purchase_quarter = (stock.purchase_date.month - 1) // 3 + 1
        return (current_quarter != purchase_quarter)
    
    def factor_load(self,standard_df):
        prices = []
        for ticker in self.tickers:
            try:
                price = standard_df[standard_df["ticker"]==ticker].sort_values("date")
                price.sort_values("date",inplace=True)
                price["prediction"] = price["adjclose"].rolling(100).mean() * 1.025
                prices.append(price)
            except Exception as e:
                print(ticker,str(e))
                continue
        sim = pd.concat(prices)
        sim = CAPM.apply(sim)
        return sim
    
    def signal(self,sim:pd.DataFrame):
        sim["rank"] = sim.groupby("date",group_keys=False)["factor"].apply(pd.qcut,q=5,labels=False,duplicates="drop")
        sim["exposure"] = [Exposure.LONG if x > 3 else Exposure.SHORT if x < 1 else Exposure.NONE for x in sim["rank"]]
        return sim.drop("rank",axis=1)