from database.adatabase import ADatabase
from extractor.fmp_extractor import FMPExtractor
from tqdm import tqdm
market = ADatabase("market")

market.connect()
sp100 = market.retrieve("sp100")
market.disconnect()

market.connect()
market.drop("balance_sheet")
for ticker in tqdm(sp100["ticker"]):
    try:
        filings = FMPExtractor.balance_sheet(ticker)
        market.store("balance_sheet",filings)
    except Exception as e:
        print(str(e))
market.create_index("balance_sheet","ticker")
market.disconnect()