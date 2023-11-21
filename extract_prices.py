from database.adatabase import ADatabase
from extractor.tiingo_extractor import TiingoExtractor
from datetime import datetime, timedelta
from tqdm import tqdm
market = ADatabase("market")
start = datetime.now() - timedelta(days=365.25*20)
end = datetime.now()

market.connect()
sp100 = market.retrieve("sp100")
market.disconnect()

market.connect()
market.drop("prices")
for ticker in tqdm(sp100[:1]["ticker"].values):
    try:
        ticker_data = TiingoExtractor.prices(ticker,start,end)[["date","adjClose"]]
        ticker_data["ticker"] = ticker
        market.store("test_prices",ticker_data)
    except Exception as e:
        print(str(e))
        continue