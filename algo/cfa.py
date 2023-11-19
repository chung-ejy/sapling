from database.adatabase import ADatabase
from processor.processor import Processor as p
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd

class CFA(object):

    def __init__(self,rolling_val,projection_weeks,rr,risk,tickers,skip):
        self.market = ADatabase("market")
        self.fed = ADatabase("fed")
        self.financial = ADatabase("financial")
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
        sims = []
        self.fed.connect()
        benchmark = p.column_date_processing(self.fed.retrieve("sp500")).rename(columns={"value":"sp500"})
        yields = p.column_date_processing(self.fed.retrieve("tyields")).rename(columns={"value":"yield1"})
        yields["yield1"] = [float(x)/100 for x in yields["yield1"]]
        sp500_projections = self.fed.retrieve("sp500_v2_projections").rename(columns={"prediction":"sp500_prediction"})
        self.fed.disconnect()
        positions = 10
        self.market.connect()
        sp100 = self.market.retrieve("sp100")
        for ticker in tqdm(self.tickers):
            try:
                prices = p.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                # financials = financial.query("simulation",{"ticker":ticker})
                # financials["prediction_quarter"] = financials["quarter"]
                # sim = p.merge(sim,financials,on=["year","quarter"])
                sim = p.merge(prices,sp500_projections,on=["year","quarter"])
                sim = p.merge(sim,benchmark,on="date")
                sim = p.merge(sim,yields,on="date").ffill().bfill()
                sim["sp500_var"] = sim["sp500"].rolling(100).var()
                sim["sp500_cov"] = sim["sp500"].rolling(100).cov(sim["adjclose"].rolling(100).mean())
                sim["market_return"] = (sim["sp500"].shift(-262) - sim["sp500"]) / sim["sp500"]
                sim["market_expected_return"] = (sim["sp500_prediction"] - sim["sp500"]) / sim["sp500"]
                sim["beta"] = sim["sp500_cov"] / sim["sp500_var"]
                sim["prediction"] = (sim["adjclose"].rolling(262).mean() - sim["adjclose"]) / sim["adjclose"]
                sim["signal"] = (sim["prediction"] - sim["adjclose"]) / sim["adjclose"] - sim["yield1"] + sim["beta"] * (sim["market_expected_return"]-sim["yield1"])
                sim["abs"] = sim["signal"].abs()
                sim["rolling"] = sim["adjclose"].rolling(self.rolling_val).mean()
                sim["std"] = sim["adjclose"].rolling(self.rolling_val).std()
                sim["risk"] = sim["std"] / sim["rolling"]
                sim["direction"] = sim["signal"] / sim["abs"]
                sim["sell_price"] = sim["adjclose"].shift(-60)
                sim["sell_date"] = sim["date"].shift(-60)
                sim["buy_price"] = sim["adjclose"].shift(-1)
                sim["bond_return"] = .05
                sim["stock_return"] = (sim["sell_price"] - sim["buy_price"])/sim["buy_price"] 
                sim["return"] = (sim["stock_return"] * 0.5 + sim["bond_return"] * 0.4 + sim["market_return"] * 0.1) * float(1/positions)
                sim = sim[sim["year"]>=2021]
                sims.append(sim)
            except Exception as e:
                print(str(e))
        self.market.disconnect()
        simulation = pd.concat(sims).merge(sp100,on="ticker",how="left")
        # trades = simulation[simulation["quarter"]==4]
        # trades = trades[trades["year"]==2023]
        trades = simulation[simulation["weekday"]==4]
        trades = trades[trades["risk"]<=self.risk]
        trades = trades[trades["abs"]>=self.rr]
        trades = trades.sort_values("date").groupby(["year","quarter","ticker"]).first().reset_index().sort_values("year")
        trades = trades.sort_values("abs").groupby(["year","quarter","GICS Sector"]).first().reset_index().sort_values("year")
        portfolio = trades[["year","quarter","return"]].groupby(["year","quarter"]).sum().reset_index()
        portfolio["return"] = portfolio["return"] + 1
        portfolio.sort_values(["year","quarter"],inplace=True)
        portfolio["cr"] = portfolio["return"].cumprod()
        return portfolio


 