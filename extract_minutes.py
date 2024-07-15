from database.adatabase import ADatabase
from extractor.alp_client_extractor import ALPClientExtractor
from processor.processor import Processor as processor
from datetime import datetime, timedelta
from tqdm import tqdm 
from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
from time import sleep
end = datetime.now()
start = datetime.now() - timedelta(days=1)
market = ADatabase("market")

market.connect()
sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",attrs={"id":"constituents"})[0].rename(columns={"Symbol":"ticker"})
tickers = ["SPY"]
tickers.extend(sp500["ticker"].values)
market.drop("prices_minute")
for ticker in tqdm(tickers):
    try:
        if "." not in ticker:
            ticker_prices = processor.column_date_processing(ALPClientExtractor(os.getenv("APCAKEY"),os.getenv("APCASECRET")).prices_minute(ticker,start,end))
            ticker_prices["ticker"] = ticker
            ticker_prices.sort_values("date",inplace=True)  
            market.store("prices_minute",ticker_prices)
            sleep(1)
    except Exception as e:
        print(ticker,str(e))
market.create_index("prices_minute","ticker")
market.disconnect()