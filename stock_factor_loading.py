from processor.processor import Processor as processor
from database.adatabase import ADatabase
from extractor.alp_client_extractor import ALPClientExtractor
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta
from dotenv import load_dotenv
from time import sleep
load_dotenv()
import os
import warnings
warnings.simplefilter(action="ignore")

factors =  ["AMZN","GOOGL","AAPL","NVDA","TSLA","MSFT","META"]
key = os.getenv("APCAKEY")
secret = os.getenv("APCASECRET")
alp_client = ALPClientExtractor(key,secret)
account = alp_client.account()
cash = float(account["cash"])
holding_period = 5
stoploss = 1
positions = 1
ranker = "average_return"
ascending = True
end = datetime.now()
start = datetime.now() - timedelta(days=365.25)
today = datetime.now()

db = ADatabase("sapling")
db.cloud_connect()
keys = db.retrieve("secrets")
db.disconnect()

def calculate_expected_return(row, factors):
    factor_loadings = [row[factor] * row[f"{factor}_beta"] for factor in factors]
    return np.mean(factor_loadings)

sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",attrs={"id":"constituents"})[0].rename(columns={"Symbol":"ticker"})

factor_dfs = []
for ticker in factors:
    try:
        ticker_prices = processor.column_date_processing(alp_client.prices(ticker,start,end))[["date","ticker","adjclose"]]
        ticker_prices["historical_return"] = ticker_prices["adjclose"].pct_change(holding_period) 
        factor_dfs.append(ticker_prices)
    except Exception as e:
        print(str(e))
        continue
factor_df = pd.concat(factor_dfs).pivot_table(index="date",columns="ticker",values="historical_return").reset_index()
factor_df

simulation = []
for ticker in sp500["ticker"]:
    try:
        ticker_prices = processor.column_date_processing(alp_client.prices(ticker,start,end))
        ticker_prices["ticker"] = ticker
        ticker_prices.sort_values("date",inplace=True)
        ticker_prices = processor.merge(ticker_prices,factor_df.copy(),on="date")
        ticker_prices["historical_return"] = ticker_prices["adjclose"].pct_change(holding_period)
        for factor in factors:
            ticker_prices[f"{factor}_covariance"] = ticker_prices["historical_return"].rolling(100).cov(ticker_prices[factor])
            ticker_prices[f"{factor}_beta"] = ticker_prices[f"{factor}_covariance"] / ticker_prices[factor].rolling(100).var()
            ticker_prices[f"{factor}_loading"] = ticker_prices[factor] * ticker_prices[f"{factor}_beta"]
        ticker_prices["average_return"] = ticker_prices["adjclose"].pct_change(holding_period).rolling(100).mean()
        ticker_prices["coev"] = ticker_prices["adjclose"].rolling(100).std() / ticker_prices["adjclose"].rolling(100).mean()
        ticker_prices["buy_date"] = ticker_prices["date"].shift(-1)
        ticker_prices["sell_date"] = ticker_prices["date"].shift(-holding_period)
        ticker_prices["buy_price"] = ticker_prices["adjclose"].shift(-1)
        ticker_prices["sell_price"] = ticker_prices["adjclose"].shift(-holding_period)
        ticker_prices["return"] = (ticker_prices["sell_price"] - ticker_prices["buy_price"]) / ticker_prices["buy_price"]
        ticker_prices["expected_return"] = ticker_prices.apply(lambda row: calculate_expected_return(row, factors), axis=1)
        simulation.append(ticker_prices)
        sleep(0.5)
    except Exception as e:
        print(ticker,str(e))
        continue
    
sim = pd.concat(simulation)

trades = sim[sim["weekday"]==4].copy()
trades = trades.merge(sp500[["ticker","GICS Sector"]],on="ticker",how="left")
trades = trades[trades["week"] % int(holding_period/5) == 0]
trades.sort_values("date",inplace=True)
iteration_trades = trades.copy().sort_values(ranker,ascending=ascending).groupby(["date"]).nth([i for i in range(positions)]).reset_index()
iteration_trades.sort_values("date",inplace=True)
recommendations = iteration_trades[iteration_trades["date"]==iteration_trades["date"].max()].copy()

for row in keys.iterrows():
    try:
        alp_client = ALPClientExtractor(row[1]["key"],row[1]["secret"])
        account = alp_client.account()
        cash = float(account["cash"])
        notional = round(math.floor(float(cash/positions)*100) / 100.00,2)
        if today.weekday() == 0 and notional > 0:
            for row in recommendations.iterrows():
                ticker = row[1]["ticker"]
                alp_client.buy(ticker,notional)
        elif today.weekday() == 4:
            alp_client.close()
        else:
            continue
    except Exception as e:
        print(str(e))
        continue