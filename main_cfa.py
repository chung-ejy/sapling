from database.adatabase import ADatabase
import pandas as pd
from processor.processor import Processor as p
from tqdm import tqdm

market = ADatabase("market")
fed = ADatabase("fed")
financial = ADatabase("financial")

fed.connect()
benchmark = p.column_date_processing(fed.retrieve("sp500")).rename(columns={"value":"sp500"})
yields = p.column_date_processing(fed.retrieve("tyields")).rename(columns={"value":"yield1"})
yields["yield1"] = [float(x)/100 for x in yields["yield1"]]
sp500_projections = fed.retrieve("sp500_projections").rename(columns={"prediction":"sp500_prediction"})
fed.disconnect()
market.connect()
sp100 = market.retrieve("sp100")
financial.connect()
sims = []
for ticker in tqdm(sp100["ticker"]):
    try:
        prices = p.column_date_processing(market.query("prices",{"ticker":ticker}))
        sim = p.merge(prices,sp500_projections,on=["year","quarter"])
        sim = p.merge(sim,benchmark,on="date")
        sim = p.merge(sim,yields,on="date")
        sim["sp500_var"] = sim["sp500"].rolling(100).var()
        sim["sp500_cov"] = sim["sp500"].rolling(100).cov(sim["adjclose"].rolling(100).mean())
        sim["market_expected_return"] = (sim["sp500_prediction"] - sim["sp500"]) / sim["sp500"]
        sim["beta"] = sim["sp500_cov"] / sim["sp500_var"]
        sim["signal"] = sim["yield1"] + sim["beta"] * (sim["market_expected_return"]-sim["yield1"])
        sim["abs"] = sim["signal"].abs()
        sim["direction"] = sim["signal"] / sim["abs"]
        sim = sim[["date","ticker","signal","abs","direction","adjclose"]].dropna()
        sims.append(sim.tail(1))
    except Exception as e:
        print(str(e))
market.disconnect()
financial.disconnect()

simulation = pd.concat(sims)
print(simulation.sort_values("abs").tail(10))
