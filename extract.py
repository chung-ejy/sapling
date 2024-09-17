from database.adatabase import ADatabase
from extractor.alp_client_extractor import ALPClientExtractor
from extractor.tiingo_extractor import TiingoExtractor
from processor.processor import Processor as processor
from datetime import datetime, timedelta
from tqdm import tqdm 
from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
from time import sleep

end = datetime.now()
start = datetime.now() - timedelta(days=365.25*20)
market = ADatabase("market")


sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",attrs={"id":"constituents"})[0].rename(columns={"Symbol":"ticker"})
tickers = []
tickers.extend(sp500["ticker"].values)
market.connect()
market.drop("prices")
for ticker in tqdm(tickers):
    try:
        ticker_data = TiingoExtractor().prices(ticker,start,end).rename(columns={"adjClose":"adjclose"})
        ticker_data["ticker"] = ticker
        market.store("prices",ticker_data)
    except Exception as e:
        print(str(e))
market.create_index("prices","ticker")
market.disconnect()