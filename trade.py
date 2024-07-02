from trader.live_trader import LiveTrader
from trading_client.alpaca_paper_client import AlpacaPaperClient
from parameters.AParameters import AParameters
from xgboost import XGBRegressor
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tqdm import tqdm
from asset.stock import Stock
from asset.bond import Bond
from asset.option import Option
import warnings
import pytz
import copy
from processor.processor import Processor as processor
from database.adatabase import ADatabase
from datetime import datetime, timedelta
from database.adatabase import ADatabase
warnings.simplefilter(action="ignore")
import pickle
sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",attrs={"id":"constituents"})[0].rename(columns={"Symbol":"ticker"})
tickers = sp500["ticker"]
db = ADatabase("sapling")



trading_client = AlpacaPaperClient()
bars = []
prices = processor.column_date_processing(trading_client.bar(tickers))
db.cloud_connect()
sim = db.retrieve("sim")
db.disconnect()
sim = prices.merge(sim[["year","quarter","ticker","GICS Sector","prediction"]],on=["year","quarter","ticker"],how="left").dropna()
sim["expected_return"] = (sim["prediction"] - sim["adjclose"]) / sim["adjclose"]
trader = LiveTrader(trading_client=trading_client,parameters=AParameters())
trader.trade(sim)