#!/usr/bin/env python
# coding: utf-8

# In[1]:


from database.adatabase import ADatabase
import pandas as pd
import matplotlib.pyplot as plt
from processor.processor import Processor as processor
from tqdm import tqdm
import warnings
warnings.simplefilter(action="ignore")
from datetime import datetime, timedelta, timezone
from xgboost import XGBRegressor
import random


# In[2]:


db = ADatabase("algo")
market = ADatabase("market")
market.connect()
russell1000 = market.retrieve("russell1000")
market.disconnect()


# In[3]:


tickers = russell1000["ticker"].values
training_year = datetime.now().year - 3
holding_period = 5
today = datetime.now()
weekday = today.weekday() - 1 if today.weekday() != 0 else 4


# In[4]:


market.connect()
prices = []
for ticker in tqdm(tickers,desc="model_prep"):
    try:
        ticker_prices = processor.column_date_processing(market.query("prices",{"ticker":ticker}))[["date","week","month","weekday","ticker","adjclose"]]
        ticker_prices.sort_values("date",inplace=True)
        ticker_prices["coefficient_of_variance"] = ticker_prices["adjclose"].rolling(100).std() / ticker_prices["adjclose"].rolling(100).mean()
        ticker_prices["buy_price"] = ticker_prices["adjclose"].shift(-1)
        ticker_prices["buy_date"] = ticker_prices["date"].shift(-1)
        ticker_prices["sell_price"] = ticker_prices["adjclose"].shift(-holding_period)
        ticker_prices["sell_date"] = ticker_prices["date"] + timedelta(days=holding_period/5*7)
        ticker_prices["return"] = (ticker_prices["sell_price"] - ticker_prices["buy_price"]) / ticker_prices ["buy_price"]
        prices.append(ticker_prices.iloc[100:])
    except Exception as e:
        print(ticker,str(e))
        continue
market.disconnect()
sim = pd.concat(prices).reset_index(drop=True)


# In[5]:


positions = 10
hedge_percentage = 0.03
sim["weight"] = (1/positions)
sim["return"] = sim["return"] * sim["weight"]
sim["hedged_return"] = [max(float(-hedge_percentage/positions),x) for x in sim["return"]]
sim["month"] = [x.month for x in sim["date"]]
sim.sort_values("date",inplace=True)
trades = sim[sim["weekday"]==4].copy()
trades = trades[trades["week"] % int(holding_period/5) == 0]
trades = processor.column_date_processing(trades)


# In[7]:


valuation_method = "coefficient_of_variance"
ascending = False


# In[8]:


try:
    iteration_trades = trades.copy().sort_values(valuation_method,ascending=ascending).groupby(["date"]).nth([i for i in range(positions)])
    portfolio = iteration_trades[["date","hedged_return"]].groupby("date").sum().reset_index()
    portfolio.sort_values("date",inplace=True)
    portfolio = portfolio[(portfolio["date"]>portfolio["date"].min()) & (portfolio["date"]<portfolio["date"].max())]
    portfolio["hedged_return"] = portfolio["hedged_return"] + 1
    portfolio["cumulative_return"] = portfolio["hedged_return"].cumprod()
    recommendations = iteration_trades[["date","sell_date","ticker","adjclose",valuation_method]].sort_values(["date"]).tail(positions)
    plt.hist(iteration_trades["hedged_return"],bins=10,align="left")
    plt.show()
    scatter = iteration_trades.sort_values("hedged_return")
    plt.scatter(scatter["coefficient_of_variance"].values,scatter["hedged_return"].values,c=scatter["month"],cmap="RdYlGn",s=10)
    plt.legend(list(iteration_trades["month"].unique()))
    plt.show()
    plt.plot(portfolio["date"].values,portfolio["cumulative_return"].values)
    plt.show()
except Exception as e:
    print(str(e))


# In[10]:


iteration_trades.sort_values("return",ascending=False).head(10)


# In[11]:


recommendations


# In[12]:


db.connect()
db.drop('recommendations')
db.store("recommendations",recommendations)
db.disconnect()

