from database.adatabase import ADatabase
from extractor.alp_extractor import ALPExtractor
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd
market = ADatabase("market")
start = datetime.now() - timedelta(days=365.25*2)
end = datetime.now() - timedelta(days=1)

print("price_extractions")
market.cloud_connect()
sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",attrs={"id":"constituents"})[0].rename(columns={"Symbol":"ticker"})
sp100 = pd.read_html("https://en.wikipedia.org/wiki/S%26P_100",attrs={"id":"constituents"})[0].rename(columns={"Symbol":"ticker"})
russell1000 = pd.read_html("https://en.wikipedia.org/wiki/Russell_1000_Index")[2].rename(columns={"Ticker":"ticker"})
market.drop("sp100")
market.store("sp100",sp100)
market.drop("sp500")
market.store("sp500",sp500)
market.drop("russell1000")
market.store("russell1000",russell1000)
market.disconnect()

tickers = russell1000["ticker"].values
market.cloud_connect()
market.drop("prices")
for ticker in tqdm(tickers):
    try:
        ticker_data = ALPExtractor.prices(ticker,start,end)
        ticker_data["ticker"] = ticker
        market.store("prices",ticker_data)
    except Exception as e:
        print(str(e))
        continue
market.create_index("prices","ticker")
market.disconnect()