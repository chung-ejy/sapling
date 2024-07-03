from trader.live_trader import LiveTrader
from trading_client.alpaca_paper_client import AlpacaPaperClient
from strategy.average_return_strategy import AverageReturnStrategy
from parameter.aparameter import AParameter
import pandas as pd
import warnings
from processor.processor import Processor as processor
from database.adatabase import ADatabase
warnings.simplefilter(action="ignore")
from time import sleep
import  os
from datetime import datetime, timedelta
from extractor.alp_client_extractor import ALPClientExtractor
from dotenv import load_dotenv
load_dotenv()
db = ADatabase("sapling")
while True:
    try:
        sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",attrs={"id":"constituents"})[0].rename(columns={"Symbol":"ticker"})
        tickers = sp500["ticker"]
        trading_client = AlpacaPaperClient()
        strategy = AverageReturnStrategy(AParameter(1))
        prices = processor.column_date_processing(trading_client.bar(tickers))
        if prices.index.size > 0:
            sim = []
            for ticker in tickers:
                try:
                    price = processor.column_date_processing(
                        ALPClientExtractor(os.getenv("APCAKEY"),os.getenv("APCASECRET")).prices_minute(
                            ticker,datetime.now() - timedelta(minutes=100),datetime.now())).sort_values("date")
                    price["average_return"] = price["adjclose"].pct_change(60)
                    sim.append(price.dropna())
                    sleep(0.1)
                except:
                    continue
            sim = pd.concat(sim).sort_values("date")
            sim = strategy.preprocessing(sim,prices)
            trader = LiveTrader(trading_client=trading_client,strategy=strategy)
            trader.trade(sim)
    except Exception as e:
        print(str(e))
    sleep(60)
