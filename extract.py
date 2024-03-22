from database.adatabase import ADatabase
from extractor.alp_client_extractor import ALPClientExtractor
from extractor.tiingo_extractor import TiingoExtractor
from processor.processor import Processor as processor
from datetime import datetime, timedelta
from tqdm import tqdm 
from dotenv import load_dotenv
load_dotenv()
import os

end = datetime.now()
start = datetime.now() - timedelta(days=365.25  *2)
market = ADatabase("market")

market.connect()
tickers = market.retrieve("sp500")["ticker"].values

market.drop("prices")
for ticker in tqdm(tickers):
    try:
        ticker_prices = processor.column_date_processing(ALPClientExtractor(os.getenv("APCAKEY"),os.getenv("APCASECRET")).prices(ticker,start,end))
        # ticker_prices = processor.column_date_processing(TiingoExtractor.prices(ticker,start,end))
        ticker_prices["ticker"] = ticker
        ticker_prices.sort_values("date",inplace=True)  
        market.store("prices",ticker_prices)
    except Exception as e:
        print(ticker,str(e))
market.create_index("prices","ticker")
market.disconnect()