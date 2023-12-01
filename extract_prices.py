from database.adatabase import ADatabase
from extractor.tiingo_extractor import TiingoExtractor
from datetime import datetime, timedelta
from tqdm import tqdm
market = ADatabase("market")
start = datetime.now() - timedelta(days=365.25*14)
end = datetime.now()

market.connect()
sp500 = market.retrieve("sp500")
market.disconnect()

market.connect()
market.drop("prices")
for ticker in tqdm(sp500["ticker"].values):
    try:
        ticker_data = TiingoExtractor.prices(ticker,start,end)[["date","adjClose"]]
        ticker_data["ticker"] = ticker
        market.store("prices",ticker_data)
    except Exception as e:
        print(str(e))
        continue
market.create_index("prices","ticker")
market.disconnect()