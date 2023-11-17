from database.adatabase import ADatabase
from processor.processor import Processor as p
from extractor.alp_extractor import ALPExtractor as alp
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
market = ADatabase("market")
market.connect()
sp100 = market.retrieve("sp100")
market.disconnect()

start = datetime.now() - timedelta(days=365)
end = datetime.now() - timedelta(days=1)


tickers = sp100["ticker"]
tickers = pd.read_csv("tickers.csv")["ticker"]

sim = []
print(tickers)
for ticker in tqdm(tickers):
    try:
        prices = p.column_date_processing(alp.prices(ticker,start,end))
        prices["prediction"] = prices["adjclose"].rolling(100).mean()
        prices["signal"] = (prices["prediction"] - prices["adjclose"]) / prices["adjclose"]
        prices["abs"] = prices["signal"].abs()
        prices["direction"] = prices["signal"] / prices["abs"]
        prices["buy_price"] = prices["adjclose"].shift(-1)
        prices["buy_date"] = prices["date"].shift(-1)
        prices["sell_price"] = prices["adjclose"].shift(-5)
        prices["sell_date"] = prices["date"].shift(-5)
        prices["return"] = (prices["sell_price"] - prices["buy_price"]) / prices["buy_price"] * prices["direction"] + 1
        sim.append(prices.iloc[100:].fillna(1))
    except Exception as e:
        print(ticker,str(e))

simulation = pd.concat(sim)
trades = simulation[simulation["weekday"]==4]
trades = trades.sort_values("abs",ascending=False).groupby(["date"]).first().reset_index()
trades.to_csv("trades.csv")
trades["cr"] = trades["return"].cumprod()
trades.sort_values("date",inplace=True)
plt.plot(trades["date"].values,trades["cr"].values)
plt.show()
print(trades.tail(1))