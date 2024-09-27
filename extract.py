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


russell1000 = pd.read_html("https://en.wikipedia.org/wiki/Russell_1000_Index")[2].rename(columns={"Symbol":"ticker"})
tickers = []
tickers.extend(russell1000["ticker"].values)
market.connect()
market.drop("prices")
for ticker in tqdm(tickers):
    try:
        ticker_data = ALPClientExtractor(os.getenv("APCAKEY"),os.getenv("APCASECRET")).prices(ticker,start,end)
        # ticker_data = TiingoExtractor().prices(ticker,start,end).rename(columns={"adjClose":"adjclose"})
        sleep(1)
        ticker_data["ticker"] = ticker
        market.store("prices",ticker_data)
    except Exception as e:
        print(str(e))
market.create_index("prices","ticker")
market.disconnect()