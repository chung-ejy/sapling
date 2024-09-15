from metric.metric import Metric
from metric.metric_factory import MetricFactory
from trading_client.alpaca_client import AlpacaClient
from trader.live_trader import LiveTrader
import pandas as pd
from processor.processor import Processor
from extractor.alp_client_extractor import ALPClientExtractor
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()
import os
import warnings
from database.adatabase import ADatabase
from datetime import datetime, timedelta
warnings.simplefilter(action="ignore")

end = datetime.now()
start = datetime.now() - timedelta(days=150)
russell1000 = pd.read_html("https://en.wikipedia.org/wiki/Russell_1000_Index")[2].rename(columns={"Symbol":"ticker"})
db = ADatabase("sapling")
tickers = russell1000["ticker"].values
chunks = [tickers[i:i + 25] for i in range(0, len(tickers), 25)]
metric = MetricFactory.build(Metric.COEFFICIENT_OF_VARIANCE)
analysis = []
all_positions = []
client = AlpacaClient()
trader = LiveTrader(metric,client)
ticker_prices = []
for chunk in chunks:
    ticker_data = ALPClientExtractor(key=os.getenv("APCAKEY"),secret=os.getenv("APCASECRET")).prices_bulk(",".join(chunk),start,end)
    for key in ticker_data["bars"].keys():
        prices = Processor.column_date_processing(pd.DataFrame(ticker_data["bars"][key]).rename(columns={"c":"adjclose","t":"date","l":"adjlow","h":"adjhigh","v":"volume"})[["date","adjclose","adjlow","adjhigh","volume"]]).sort_values("date")
        prices = metric.create_metric(prices)
        prices["ticker"] = key
        ticker_prices.append(prices)
recommendations = pd.concat(ticker_prices).dropna().sort_values("date")
account = client.account()
positions = client.positions()
print(positions)
# positions = []
# trader.trade(account,positions,end,recommendations)