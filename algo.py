from database.adatabase import ADatabase
import pandas as pd
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
from processor.processor import Processor as processor
from tqdm import tqdm
import warnings
warnings.simplefilter(action="ignore")
import pickle

## database init
db = ADatabase("algo")
market = ADatabase("market")
fed = ADatabase("fed")
market.connect()
sp100 = market.retrieve("sp100")
market.disconnect()

training_year = 2020
holding_period = 65
rr = 0
risk = 1
tickers = sp100["ticker"].values
remodel = False
factors = ["rolling_10","rolling_20","rolling_60","rolling_100"]
## model_data
market.connect()
model_data = []
for ticker in tqdm(tickers,desc="model_prep"):
    try:
        ticker_prices = processor.column_date_processing(market.query("prices",{"ticker":ticker}))
        ticker_prices.sort_values("date",inplace=True)
        ticker_prices["rolling_10"] = ticker_prices["adjclose"].rolling(10).mean()
        ticker_prices["rolling_20"] = ticker_prices["adjclose"].rolling(20).mean()
        ticker_prices["rolling_60"] = ticker_prices["adjclose"].rolling(60).mean()
        ticker_prices["rolling_100"] = ticker_prices["adjclose"].rolling(100).mean()
        ticker_prices["y"] = ticker_prices["adjclose"].shift(-holding_period)
        model_data.append(ticker_prices)
    except:
        continue
market.disconnect()

## ai
training_data = pd.concat(model_data)
model_data = training_data[(training_data["year"]==training_year)].dropna()

db.connect()
if remodel == True:
    db.drop("model")
    model = XGBRegressor(booster="dart",learning_rate=1)
    model.fit(model_data[factors],model_data["y"])
    pickled = pickle.dumps(model)
    db.store("model",pd.DataFrame([{"model":pickled}]))
else:
    try:
        model = pickle.loads(db.retrieve("model")["model"].iloc[0])
    except:
        print("no model")
db.disconnect()

simulation = training_data[training_data["year"]>=2021]
simulation["prediction"] = model.predict(simulation[factors])
bt_data = []
for ticker in tqdm(simulation["ticker"].unique(),desc="backtest_prep"):
    prices = simulation[simulation["ticker"]==ticker]
    prices.sort_values("date",inplace=True)
    prices["signal"] = (prices["prediction"] - prices["adjclose"]) / prices["adjclose"]
    prices["std"] = prices["adjclose"].rolling(holding_period).std()
    prices["rolling"] = prices["adjclose"].rolling(holding_period).mean()
    prices["risk"] = prices["std"] / prices["rolling"]
    prices["sell_price"] = prices["adjclose"].shift(-holding_period)
    prices["sell_date"] = prices["date"].shift(-holding_period)
    bt_data.append(prices)
sim = pd.concat(bt_data)

## cfa
fed.connect()
benchmark = processor.column_date_processing(fed.retrieve("sp500")).rename(columns={"value":"sp500"})
yields = processor.column_date_processing(fed.retrieve("tyields")).rename(columns={"value":"yield1"})
yields["yield1"] = [(1+float(x)/100) ** (holding_period/365) - 1 for x in yields["yield1"]]
sp500_projections = fed.retrieve("sp500_v2_projections").rename(columns={"prediction":"sp500_prediction"})
fed.disconnect()

sim = processor.merge(sim,sp100,on="ticker")
sim = processor.merge(sim,sp500_projections,on=["year","quarter"])
sim = processor.merge(sim,benchmark,on="date")
sim = processor.merge(sim,yields,on="date").ffill().bfill()

sim["sp500_var"] = sim["sp500"].rolling(100).var()
sim["sp500_cov"] = sim["sp500"].rolling(100).cov(sim["adjclose"].rolling(50).mean())
sim["market_expected_return"] = (sim["sp500_prediction"] - sim["sp500"]) / sim["sp500"]
sim["beta"] = sim["sp500_cov"] / sim["sp500_var"]
sim["signal"] = (sim["signal"]) - sim["yield1"] + sim["beta"] * (sim["market_expected_return"]-sim["yield1"])

## post cfa
sim["abs"] = sim["signal"].abs()
sim["direction"] = sim["signal"] / sim["abs"]
positions = len(sim["GICS Sector"].unique())
sim["return"] = (sim["sell_price"] - sim["adjclose"]) / sim ["adjclose"] * (1/positions) * sim["direction"]
sim.sort_values("date",inplace=True)

## backtest
trades = sim[sim["weekday"]==4]
trades = trades[trades["abs"]>=rr]
trades = trades[trades["risk"]<=risk]
week_mod = int(holding_period / 5)

if week_mod > 1:
    trades = trades[trades["week"] % week_mod + 1 == 1]
trades = trades.sort_values("abs").groupby(["date","GICS Sector"]).first().reset_index()

# analysis
trades = processor.column_date_processing(trades[["date","std","ticker","GICS Sector","adjclose","return"]])

plt.scatter(trades["std"],trades["return"],s=10)
plt.show()

portfolio = trades[["date","return"]].groupby("date").sum().reset_index()
portfolio = processor.merge(portfolio,benchmark,on="date").dropna()
portfolio["bcr"] = (portfolio["sp500"] - portfolio["sp500"].iloc[0]) / portfolio["sp500"].iloc[0] + 1
portfolio["return"] = portfolio["return"] + 1
portfolio["cr"] = portfolio["return"].cumprod()

plt.plot(portfolio["date"].values,portfolio["cr"].values)
plt.plot(portfolio["date"].values,portfolio["bcr"].values)
plt.show()

recommendations = trades.tail(positions)

db.connect()
db.store("portfolio",portfolio)
db.store("trades",trades)
db.store("recommendations",recommendations)
db.disconnect()

portfolio.to_csv("portfolio.csv")
trades.to_csv("trades.csv")
recommendations.to_csv("recommendations.csv")