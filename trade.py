from trader.live_trader import LiveTrader
from trading_client.alpaca_paper_client import AlpacaPaperClient
from parameters.AParameters import AParameters
import pandas as pd
import warnings
from processor.processor import Processor as processor
from database.adatabase import ADatabase
warnings.simplefilter(action="ignore")
from time import sleep

db = ADatabase("sapling")
while True:
    try:
        sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",attrs={"id":"constituents"})[0].rename(columns={"Symbol":"ticker"})
        tickers = sp500["ticker"]
        trading_client = AlpacaPaperClient()
        prices = processor.column_date_processing(trading_client.bar(tickers))
        if prices.index.size > 0:
            db.cloud_connect()
            sim = db.retrieve("sim")
            db.disconnect()
            sim = prices.merge(sim[["year","quarter","ticker","GICS Sector","prediction"]],on=["year","quarter","ticker"],how="left").dropna()
            sim["expected_return"] = (sim["prediction"] - sim["adjclose"]) / sim["adjclose"]
            trader = LiveTrader(trading_client=trading_client,parameters=AParameters())
            trader.trade(sim)
    except Exception as e:
        print(str(e))
    sleep(60)
