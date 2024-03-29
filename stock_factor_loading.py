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

simulation = []
for ticker in sp500["ticker"]:
    try:
        ticker_prices = processor.column_date_processing(alp_client.prices(ticker,start,end))
        ticker_prices["ticker"] = ticker
        ticker_prices.sort_values("date",inplace=True)
        ticker_prices["average_return"] = ticker_prices["adjclose"].pct_change(holding_period).rolling(100).mean()
        ticker_prices["coev"] = ticker_prices["adjclose"].rolling(100).std() / ticker_prices["adjclose"].rolling(100).mean()
        ticker_prices.dropna(inplace=True)
        ticker_prices["buy_date"] = ticker_prices["date"].shift(-1)
        ticker_prices["sell_date"] = ticker_prices["date"].shift(-holding_period)
        ticker_prices["buy_price"] = ticker_prices["adjclose"].shift(-1)
        ticker_prices["sell_price"] = ticker_prices["adjclose"].shift(-holding_period)
        ticker_prices["return"] = (ticker_prices["sell_price"] - ticker_prices["buy_price"]) / ticker_prices["buy_price"]
        simulation.append(ticker_prices)
        sleep(0.5)
    except Exception as e:
        print(ticker,str(e))
        continue
    
sim = pd.concat(simulation)

trades = sim[sim["weekday"]==4].copy()
trades = trades[trades["week"] % int(holding_period/5) == 0]
trades.sort_values("date",inplace=True)
iteration_trades = trades.copy().sort_values(ranker,ascending=ascending).groupby("date").nth([i for i in range(positions)]).reset_index()
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