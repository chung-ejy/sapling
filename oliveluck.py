#!/usr/bin/env python
# coding: utf-8

# In[7]:


from database.adatabase import ADatabase
import pandas as pd
from modeler.modeler import Modeler as m
import matplotlib.pyplot as plt
from processor.processor import Processor as processor
from tqdm import tqdm
import warnings
warnings.simplefilter(action="ignore")
import pickle
from datetime import datetime, timedelta, timezone
from extractor.alp_extractor import ALPExtractor
from CFA.cfa import CFA as cfa


# In[8]:


db = ADatabase("algo")
market = ADatabase("market")
fed = ADatabase("fed")
market.connect()
sp500 = market.retrieve("sp500")
market.disconnect()
alp = ALPExtractor()


# In[9]:


holding_period = 5
tickers = sp500["ticker"].values
positions = 10
hedge_percentage = 0.05
training_year = datetime.now().year - 3
today = datetime.now()
weekday = today.weekday() - 1 if today.weekday() != 0 else 4
week = today.isocalendar()[1] if today.weekday() != 0 else today.isocalendar()[1] - 1
week_mod = int(week % (holding_period/5))
print(week_mod,week)


# In[10]:


market.connect()
prices = []
for ticker in tqdm(tickers,desc="model_prep"):
    try:
        ticker_prices = processor.column_date_processing(market.query("prices",{"ticker":ticker}))
        ticker_prices.sort_values("date",inplace=True)
        simulation = ticker_prices.copy()
        simulation.sort_values("date",inplace=True)
        simulation["historical_return"] = (simulation["adjclose"] - simulation["adjclose"].shift(100)) / simulation["adjclose"].shift(100)
        simulation["historical_volatility"] = simulation["adjclose"].rolling(100).std() / simulation["adjclose"].rolling(100).mean()
        simulation["historical_return_to_risk"] = simulation["historical_return"] / simulation["historical_volatility"]
        simulation["volatility"] = (simulation["adjclose"].rolling(holding_period).std() / simulation["adjclose"].rolling(holding_period).mean())
        simulation["current_return"] = (simulation["adjclose"] - simulation["adjclose"].shift(holding_period)) / simulation["adjclose"].shift(holding_period)
        simulation["return_to_risk"] = simulation["current_return"] / simulation["volatility"]
        simulation["expected_return"] = simulation["historical_return_to_risk"] * simulation["volatility"]
        simulation = cfa.cfa(simulation,holding_period)
        simulation["buy_price"] = simulation["adjclose"]
        simulation["buy_date"] = simulation["date"].shift(-1)
        simulation["sell_price"] = simulation["adjclose"].shift(-holding_period)
        simulation["sell_date"] = simulation["date"] + timedelta(days=int(holding_period /5) * 7)
        simulation["return"] = (simulation["sell_price"] - simulation["buy_price"]) / simulation ["buy_price"] * (1/positions) *0.99
        simulation["return"] = [max(float(-hedge_percentage/positions),x) for x in simulation["return"]]
        prices.append(simulation)
    except Exception as e:
        print(ticker,str(e))
        continue
market.disconnect()


# In[11]:


sim = pd.concat(prices).reset_index(drop=True)
sim.sort_values("date",inplace=True)
sim = processor.merge(sim,sp500,on="ticker")
fed.connect()
bench = fed.retrieve("sp500")
bench["date"] = pd.to_datetime(bench["date"],utc=True)
bench["value"] = [float(x) for x in bench["value"]]
fed.disconnect()
trades = sim[sim["weekday"]==weekday].copy()
trades = trades[trades["week"] % int(holding_period/5) == week_mod]
trades = processor.column_date_processing(trades)


# In[12]:


## backtest
valuation_methods = ["excess_return"
                     ,"historical_return"
                     ,"historical_volatility"
                     ,"historical_return_to_risk"
                     ,"volatility"
                     ,"current_return"
                     ,"return_to_risk"
                     ,"expected_return"]
reports = []
for valuation_method in tqdm(valuation_methods):
    try:
        iteration_trades = trades.copy().sort_values(valuation_method,ascending=False).groupby(["date"]).nth([i for i in range(positions)]).reset_index()
        portfolio = iteration_trades[["date","return"]].groupby("date").sum().reset_index()
        portfolio.sort_values("date",inplace=True)
        portfolio["year"] = [x.year for x in portfolio["date"]]
        portfolio = portfolio[(portfolio["date"]<portfolio["date"].max()) & (portfolio["year"]>=training_year)]
        portfolio["return"] = portfolio["return"] + 1
        portfolio["cumulative_return"] = portfolio["return"].cumprod()
        portfolio = processor.column_date_processing(portfolio)
        portfolio = processor.merge(portfolio,bench.copy(),on="date")
        portfolio.dropna(inplace=True)
        portfolio["bench_cum_return"] = (portfolio["value"] - portfolio["value"].iloc[0]) / portfolio["value"].iloc[0] + 1
        portfolio["beta"] = portfolio["cumulative_return"].cov(portfolio["value"])
        portfolio["treynor"] = portfolio["cumulative_return"] / portfolio["beta"]
        portfolio["excess_return"] = portfolio["cumulative_return"] - portfolio["bench_cum_return"]
        portfolio["valuation_method"] = valuation_method
        reports.append(portfolio[["valuation_method","excess_return"]].tail(1))
    except Exception as e:
        print(str(e))
        continue


# In[13]:


report = pd.concat(reports)


# In[14]:


report.sort_values("excess_return",ascending=False)


# In[15]:


valuation_method = "historical_volatility"


# In[16]:


iteration_trades = trades.copy().sort_values(valuation_method,ascending=False).groupby(["date"]).nth([i for i in range(positions)]).reset_index()
iteration_trades = iteration_trades[["date","sell_date","ticker","adjclose","buy_price","sell_price",valuation_method,"return"]]
portfolio = iteration_trades[["date","return"]].groupby("date").sum().reset_index()
portfolio.sort_values("date",inplace=True)
portfolio["year"] = [x.year for x in portfolio["date"]]
portfolio = portfolio[(portfolio["date"]<portfolio["date"].max()) & (portfolio["year"]>=training_year)]
portfolio["return"] = portfolio["return"]  + 1
portfolio["cumulative_return"] = portfolio["return"].cumprod()
portfolio = processor.column_date_processing(portfolio)
portfolio = processor.merge(portfolio,bench.copy(),on="date")
portfolio.dropna(inplace=True)
portfolio["bench_cum_return"] = (portfolio["value"] - portfolio["value"].iloc[0]) / portfolio["value"].iloc[0] + 1
portfolio["excess_return"] = portfolio["cumulative_return"] - portfolio["bench_cum_return"]
recommendations = iteration_trades[["date","sell_date","ticker","adjclose",valuation_method]].sort_values(["date"]).tail(positions)
plt.plot(portfolio["date"].values,portfolio["cumulative_return"].values)
plt.plot(portfolio["date"].values,portfolio["bench_cum_return"].values)
plt.show()


# In[17]:


portfolio.sort_values("date",ascending=False)


# In[18]:


iteration_trades.sort_values("return",ascending=False).head(10)


# In[19]:


recommendations


# In[28]:


db.connect()
db.drop('portfolio')
db.drop('trades')
db.drop('recommendations')
db.store("portfolio",portfolio)
db.store("trades",iteration_trades)
db.store("recommendations",recommendations)
db.disconnect()

