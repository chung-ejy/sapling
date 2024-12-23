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
start = datetime.now() - timedelta(days=365.25*4)
market = ADatabase("market")


sse = pd.read_html("https://en.wikipedia.org/wiki/SSE_50_Index",attrs={"id":"constituents"})[0]
print(sse)
tickers = []
tickers.extend(sse["Ticker symbol"].values)
tickers = [x.split(" ")[1] for x in tickers]
market.connect()
market.drop("sse_prices")
for ticker in tqdm(tickers[:10]):
    try:
        symbol = str(ticker)+".SS"
        print(symbol)
        ticker_data = web.DataReader(symbol, 'yahoo', start=start, end=end).reset_index()
        ticker_data["ticker"] = str(ticker)
        market.store("sse_prices",ticker_data)
    except Exception as e:
        print(str(e))
market.create_index("sse_prices","ticker")
market.disconnect()
