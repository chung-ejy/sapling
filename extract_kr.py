from database.adatabase import ADatabase
import pandas_datareader.data as web
from datetime import datetime, timedelta
from tqdm import tqdm 
from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
from time import sleep

end = datetime.now()
start = datetime.now() - timedelta(days=365.25*14)
market = ADatabase("market")


kospi = pd.read_csv("kospi.csv").rename(columns={"Issue code":"ticker"})
tickers = []
tickers.extend(kospi["ticker"].values)
market.connect()
market.drop("kr_prices")
for ticker in tqdm(tickers):
    try:
        ticker_data = web.DataReader(str(ticker).zfill(6), 'naver', start=start, end=end).reset_index()
        ticker_data["ticker"] = str(ticker)
        market.store("kr_prices",ticker_data)
    except Exception as e:
        print(str(e))
market.create_index("kr_prices","ticker")
market.disconnect()