from database.adatabase import ADatabase
from extractor.alp_paper_extractor import ALPPaperExtractor
from processor.processor import Processor as processor
from datetime import datetime, timedelta
from tqdm import tqdm 

end = datetime.now()
start = datetime.now() - timedelta(days=365.25*2)
market = ADatabase("market")

market.connect()
tickers = market.retrieve("russell1000")["ticker"].values

market.drop("prices")
for ticker in tqdm(tickers):
    try:
        ticker_prices = processor.column_date_processing(ALPPaperExtractor().prices(ticker,start,end))
        ticker_prices["ticker"] = ticker
        ticker_prices.sort_values("date",inplace=True)  
        market.store("prices",ticker_prices)
    except Exception as e:
        print(ticker,str(e))
market.disconnect()