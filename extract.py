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
start = datetime.now() - timedelta(days=365.25*2)
market = ADatabase("market")


sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",attrs={"id":"constituents"})[0].rename(columns={"Symbol":"ticker"})
tickers = []
tickers.extend(sp500["ticker"].values)
market.connect()
market.drop("prices")
chunks = [tickers[i:i + 10] for i in range(0, len(tickers), 10)]
for chunk in tqdm(chunks):
    try:
        ticker_data = ALPClientExtractor(key=os.getenv("APCAKEY"),secret=os.getenv("APCASECRET")).prices_bulk(",".join(chunk),start,end)
        for key in tqdm(ticker_data["bars"].keys()):
            prices = pd.DataFrame(ticker_data["bars"][key]).rename(columns={"c":"adjclose","t":"date","l":"adjlow","h":"adjhigh","v":"volume"})[["date","adjclose","adjlow","adjhigh","volume"]]
            prices["ticker"] = key
            market.store("prices",prices)
    except Exception as e:
        print(str(e))
market.create_index("prices","ticker")
market.disconnect()