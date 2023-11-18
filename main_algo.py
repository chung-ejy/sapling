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
rolling_val = 100
tickers = sp100["ticker"].values
# tickers = pd.read_csv("tickers.csv")["ticker"]
rr = 0.00
std = 100
sim = []
shuffle(tickers)
for ticker in tqdm(tickers[:10]):
    try:
        prices = p.column_date_processing(alp.prices(ticker,start,end))
        prices["prediction"] = prices["adjclose"].rolling(rolling_val).mean()
        # prices["prediction"] = prices["adjclose"].shift(rolling_val)
        prices["std"] = prices["adjclose"].rolling(rolling_val).std()
        prices["signal"] = (prices["prediction"] - prices["adjclose"]) / prices["adjclose"]
        prices["abs"] = prices["signal"].abs()
        prices["direction"] = prices["signal"] / prices["abs"]
        prices["buy_price"] = prices["adjclose"].shift(-1)
        prices["buy_date"] = prices["date"].shift(-1)
        prices["sell_price"] = prices["adjclose"].shift(-5)
        # prices["sell_price"] = prices["buy_price"] * (1 + 0.05 * prices["direction"] * -1)
        prices["sell_date"] = prices["date"].shift(-5)
        prices["return"] = (prices["sell_price"] - prices["buy_price"]) / prices["buy_price"] * prices["direction"] + 1
        sim.append(prices.iloc[100:].fillna(1))
    except Exception as e:
        print(ticker,str(e))

simulation = pd.concat(sim)
trades = simulation[simulation["weekday"]==4]
trades = trades[trades["std"]<=std]
trades = trades[trades["abs"]>=rr]
trades = trades.sort_values("abs",ascending=False).groupby(["date"]).first().reset_index()
trades.to_csv("trades.csv")
trades["cr"] = trades["return"].cumprod() * 100
trades.sort_values("date",inplace=True)
plt.plot(trades["date"].values,trades["cr"].values)
plt.show()


seats = trades.tail(1)
account = alp.account()
cash = float(account["cash"])

for row in seats.iterrows():
    direction = row[1]["direction"]
    ticker = row[1]["ticker"]
    adjclose = row[1]["adjclose"]
    date = row[1]["date"]
    qty = int(cash/adjclose)
    amount = qty * adjclose
    if direction == 1:
        print(date,ticker,adjclose,qty,amount,"buy")
        # alp.buy(ticker,qty)
    else:
        print(date,ticker,adjclose,qty,amount,"sell")
        # alp.sell(ticker,qty)

if live:
    alp.close()
    sleep(300)
    for row in seats.iterrows():
        direction = row[1]["direction"]
        ticker = row[1]["ticker"]
        adjclose = row[1]["adjclose"]
        date = row[1]["date"]
        qty = int(cash/adjclose)
        amount = qty * adjclose
        if direction == 1:
            print(date,ticker,adjclose,qty,amount,"buy")
            alp.buy(ticker,qty)
        else:
            print(date,ticker,adjclose,qty,amount,"sell")
            alp.sell(ticker,qty)     