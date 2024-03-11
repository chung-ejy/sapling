from database.adatabase import ADatabase
from extractor.alp_paper_extractor import ALPPaperExtractor
from processor.processor import Processor
from datetime import datetime, timedelta

end = datetime.now()
start = datetime.now() - timedelta(days=365.25*2)
market = ADatabase("market")

market.connect()
tickers = market.retrieve("russell1000")["ticker"].values
market.disconnect()

for ticker in tickers[:1]:
    print(ticker)