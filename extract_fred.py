from extractor.fred_extractor import FREDExtractor
from datetime import datetime, timedelta
from database.adatabase import ADatabase

fred = ADatabase("fred")
start = datetime.now() - timedelta(days=365.25*10)
end = datetime.now()
sp500 = FREDExtractor.sp500(start,end)
market_yield = FREDExtractor.market_yield(start,end)
fred.connect()
fred.drop("sp500")
fred.drop("market_yield")
fred.store("sp500",sp500)
fred.store("market_yield",market_yield)
fred.disconnect()