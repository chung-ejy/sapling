from database.adatabase import ADatabase
from processor.processor import Processor as p
from extractor.alp_extractor import ALPExtractor as alp
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
from random import shuffle
from time import sleep

market = ADatabase("market")
market.connect()
sp100 = market.retrieve("sp100")
market.disconnect()

start = datetime.now() - timedelta(days=365) - timedelta(days=140)
end = datetime.now() - timedelta(days=1)

live = False
rolling_val = 20
# tickers = sp100["ticker"].values
tickers = pd.read_csv("tickers.csv")["ticker"]
rr = 0.00
std = 100
sim = []
for ticker in tqdm(tickers[::6]):
    try:
        prices = p.column_date_processing(alp.prices(ticker,start,end))
        prices["prediction"] = prices["adjclose"].rolling(rolling_val).mean()
        prices["std"] = prices["adjclose"].rolling(rolling_val).std()
        prices["signal"] = (prices["prediction"] - prices["adjclose"]) / prices["adjclose"]
        prices["abs"] = prices["signal"].abs()
        prices["direction"] = prices["signal"] / prices["abs"]
        prices["buy_price"] = prices["adjclose"]
        prices["buy_date"] = prices["date"]
        prices["sell_price"] = prices["adjclose"].shift(-1)
        prices["sell_date"] = prices["date"].shift(-1)
        prices["return"] = (prices["sell_price"] - prices["buy_price"]) / prices["buy_price"] * prices["direction"] + 1
        sim.append(prices.iloc[100:].fillna(1))
    except Exception as e:
        print(ticker,str(e))

simulation = pd.concat(sim)
trades = simulation[simulation["weekday"] % 1 == 0]
trades = trades[trades["std"]<=std]
trades = trades[trades["abs"]>=rr]
trades = trades.sort_values("abs",ascending=False).groupby(["date"]).first().reset_index()
trades.to_csv("trades.csv")
trades["cr"] = trades["return"].cumprod() * 100
trades.sort_values("date",inplace=True)
plt.plot(trades["date"].values,trades["cr"].values)
plt.show()