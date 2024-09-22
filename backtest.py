from metric.metric import Metric
from metric.metric_factory import MetricFactory
from trading_client.local_client import LocalClient
from trader.local_trader import LocalTrader
import pandas as pd
from tqdm import tqdm
import warnings
from database.adatabase import ADatabase
warnings.simplefilter(action="ignore")

russell1000 = pd.read_html("https://en.wikipedia.org/wiki/Russell_1000_Index")[2].rename(columns={"Symbol":"ticker"})
db = ADatabase("sapling")
tickers = russell1000["ticker"].values

metrics = [MetricFactory.build(x) for x in Metric]
analysis = []
all_positions = []
db.connect()
db.drop("positions")
clusters = db.retrieve("clusters")      
for metric in tqdm(metrics):
    client = LocalClient()
    trader = LocalTrader(metric,client)
    recommendations = trader.preprocessing(tickers)
    recommendations = recommendations.merge(clusters,on="ticker",how="left")
    for position in [10]:
        for boolean in [True,False]:
            metric.ascending = boolean
            metric.positions = position
            account = {"portfolio_value":100}
            positions = []
            for date in recommendations["date"].unique():
                account,positions = trader.trade(account,positions,date,recommendations)
                if len(positions) > 0:
                    db.store("positions",pd.DataFrame(positions))
            account["metric"] = metric.name
            account["boolean"] = boolean
            account["positions"] = position
            analysis.append(account)
db.disconnect()
a = pd.DataFrame(analysis).sort_values("portfolio_value",ascending=False)
print(a)

