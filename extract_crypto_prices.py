from database.adatabase import ADatabase
from extractor.alp_paper_extractor import ALPPaperExtractor
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd

market = ADatabase("market")
start = datetime.now() - timedelta(days=10)
end = datetime.now()

tickers = ["BTC/USD"]
market.connect()
market.drop("crypto")
for ticker in tqdm(tickers):
    try:
        ticker_data = ALPPaperExtractor().crypto_prices(ticker,start,end)
        ticker_data["ticker"] = ticker
        market.store("crypto",ticker_data)
    except Exception as e:
        print(str(e))
        continue
market.create_index("crypto","ticker")
market.disconnect()