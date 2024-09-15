from metric.metric import Metric
from metric.metric_factory import MetricFactory
from trading_client.local_client import LocalClient
from trader.local_trader import LocalTrader
import pandas as pd
from processor.processor import Processor
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
for metric in tqdm(metrics):
    client = LocalClient()
    trader = LocalTrader(metric,client)
    recommendations = trader.preprocessing(tickers)
    for position in [1,10]:
        for boolean in [True,False]:
            metric.ascending = boolean
            metric.positions = position
            account = {"portfolio_value":100}
            positions = []
            for date in recommendations["date"].unique():
                account,positions = trader.trade(account,positions,date,recommendations)
            account["metric"] = metric.name
            account["boolean"] = boolean
            account["positions"] = position
            analysis.append(account)
a = pd.DataFrame(analysis).sort_values("portfolio_value",ascending=False)
print(a)