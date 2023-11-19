from database.adatabase import ADatabase
import pandas as pd
from processor.processor import Processor as p
from tqdm import tqdm
import matplotlib.pyplot as plt

market = ADatabase("market")
fed = ADatabase("fed")
financial = ADatabase("financial")

fed.connect()
benchmark = p.column_date_processing(fed.retrieve("sp500")).rename(columns={"value":"sp500"})
yields = p.column_date_processing(fed.retrieve("tyields")).rename(columns={"value":"yield1"})
yields["yield1"] = [float(x)/100 for x in yields["yield1"]]
sp500_projections = fed.retrieve("sp500_v2_projections").rename(columns={"prediction":"sp500_prediction"})
fed.disconnect()
market.connect()
sp100 = market.retrieve("sp100")
financial.connect()
sims = []
positions = 10

for ticker in tqdm(sp100["ticker"]):
    try:
        prices = p.column_date_processing(market.query("prices",{"ticker":ticker}))
        financials = financial.query("simulation",{"ticker":ticker})
        financials["prediction_quarter"] = financials["quarter"]
        sim = p.merge(prices,sp500_projections,on=["year","quarter"])
        sim = p.merge(sim,financials,on=["year","quarter"])
        sim = p.merge(sim,benchmark,on="date")
        sim = p.merge(sim,yields,on="date").ffill().bfill()
        sim["sp500_var"] = sim["sp500"].rolling(100).var()
        sim["sp500_cov"] = sim["sp500"].rolling(100).cov(sim["adjclose"].rolling(100).mean())
        sim["market_return"] = (sim["sp500"].shift(-262) - sim["sp500"]) / sim["sp500"]
        sim["market_expected_return"] = (sim["sp500_prediction"] - sim["sp500"]) / sim["sp500"]
        sim["beta"] = sim["sp500_cov"] / sim["sp500_var"]
        # sim["signal"] = (sim["adjclose"].rolling(262).mean() - sim["adjclose"]) / sim["adjclose"] - sim["yield1"] + sim["beta"] * (sim["market_expected_return"]-sim["yield1"])
        sim["signal"] = (sim["prediction"] - sim["adjclose"]) / sim["adjclose"] - sim["yield1"] + sim["beta"] * (sim["market_expected_return"]-sim["yield1"])
        sim["abs"] = sim["signal"].abs()
        sim["direction"] = sim["signal"] / sim["abs"]
        sim["sell_price"] = sim["adjclose"].shift(-262)
        sim["sell_date"] = sim["date"].shift(-262)
        sim["buy_price"] = sim["adjclose"].shift(-1)
        sim["bond_return"] = .05
        sim["stock_return"] = (sim["sell_price"] - sim["buy_price"])/sim["buy_price"] 
        sim["return"] = (sim["stock_return"] * 0.5 + sim["bond_return"] * 0.4 + sim["market_return"] * 0.1) * float(1/positions)
        sim = sim[sim["year"]>=2021][["year","quarter","prediction_quarter","date","week","weekday","ticker","signal","abs","direction","adjclose","buy_price","sell_price","sell_date","return"]]
        sims.append(sim)
    except Exception as e:
        print(str(e))
market.disconnect()
financial.disconnect()


simulation = pd.concat(sims).merge(sp100,on="ticker",how="left")
trades = simulation[simulation["quarter"]==4]
trades = trades[trades["weekday"]==4]
trades = trades[trades["year"]==2023]
trades = trades.sort_values("date").groupby(["year","ticker"]).last().reset_index().sort_values("year")
trades = trades.sort_values("abs").groupby(["year","GICS Sector"]).nth([i for i in range(2)]).reset_index().sort_values("year")
trades.to_csv("cfa_trades.csv")
print(trades)
# portfolio = trades[["year","return"]].groupby(["year"]).sum()
# portfolio["return"] = portfolio["return"] + 1
# portfolio.sort_values("year",inplace=True)
# portfolio["cr"] = portfolio["return"].cumprod()
# plt.plot(portfolio["cr"])
# plt.show()
# print(trades.sort_values("date").tail(positions))