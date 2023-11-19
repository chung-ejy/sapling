from database.adatabase import ADatabase
from processor.processor import Processor as p
from extractor.alp_extractor import ALPExtractor as alp
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
from random import shuffle
from time import sleep

class Algo(object):

    def __init__(self,rolling_val,projection_weeks,rr,risk,tickers,skip):
        self.market = ADatabase("market")
        self.start = datetime.now() - timedelta(days=365) - timedelta(days=rolling_val/5*7)
        self.end = datetime.now() - timedelta(days=1)
        self.rolling_val = rolling_val
        self.tickers = tickers
        self.projection_weeks = projection_weeks
        self.projection_days = projection_weeks * 5
        self.rr = rr
        self.risk = risk
        self.skip = skip

    
    def algo(self):
        sim = []
        self.market.connect()
        for ticker in self.tickers[::self.skip]:
            try:
                prices = p.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                prices["prediction"] = prices["adjclose"].rolling(self.rolling_val).mean()
                prices["std"] = prices["adjclose"].rolling(self.rolling_val).std()
                prices["risk"] = prices["std"] / prices["prediction"]
                prices["signal"] = (prices["prediction"] - prices["adjclose"]) / prices["adjclose"]
                prices["abs"] = prices["signal"].abs()
                prices["direction"] = prices["signal"] / prices["abs"]
                prices["buy_price"] = prices["adjclose"].shift(-1)
                prices["buy_date"] = prices["date"].shift(-1)
                prices["sell_price"] = prices["adjclose"].shift(-self.projection_days)
                prices["sell_date"] = prices["date"].shift(-self.projection_days)
                prices["return"] = (prices["sell_price"] - prices["buy_price"]) / prices["buy_price"] * prices["direction"] + 1
                sim.append(prices.iloc[self.rolling_val:].fillna(1))
            except Exception as e:
                continue
        self.market.disconnect()
        simulation = pd.concat(sim)
        trades = simulation[simulation["weekday"]==4]
        trades = trades[(trades["week"] % self.projection_weeks) + 1 == 1]
        trades = trades[trades["risk"]<=self.risk]
        trades = trades[trades["abs"]>=self.rr]
        trades = trades.sort_values("abs",ascending=False).groupby(["date"]).first().reset_index()
        trades["cr"] = trades["return"].cumprod() * 100
        trades.sort_values("date",inplace=True)
        return trades


 