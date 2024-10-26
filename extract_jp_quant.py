from extractor.jp_quant_extractor import JPQuantExtractor
from database.adatabase import ADatabase
import pandas as pd
import warnings
from datetime import datetime, timedelta
from tqdm import tqdm

warnings.simplefilter(action="ignore")
db = ADatabase("jp_quant")
tse_issues = pd.read_excel("tse_issues.xls")
simplified_issues = tse_issues[["Local Code","Name (English)",'Size (New Index Series)']]
simplified_issues.rename(columns={
    "Local Code":"ticker"
    ,"Name (English)":"name"
    ,'Size (New Index Series)':"size"
},inplace=True)
groups = ['TOPIX Mid400','TOPIX Large70','TOPIX Core30']
core_500 = simplified_issues[simplified_issues["size"].isin(groups)]
db.connect()
db.drop("core500")
db.store("core500",core_500)
db.disconnect()

start = (datetime.now() - timedelta(days=365*2)).strftime("%Y%m%d")
end = datetime.now().strftime("%Y%m%d")
token = JPQuantExtractor.refresh_token()
refreshToken = token["refreshToken"]
id_token = JPQuantExtractor.id_token(refreshToken)["idToken"]
db.connect()
db.drop("prices")
for ticker in tqdm(core_500["ticker"]):
    filled_ticker = str(ticker).ljust(5, '0')
    ticker_prices = pd.DataFrame(JPQuantExtractor.prices(id_token,filled_ticker,start,end)["daily_quotes"]).rename(columns={"Date":"date","AdjustmentClose":"adjclose"})
    ticker_prices["ticker"] = str(ticker)
    db.store("prices",ticker_prices)
db.create_index("prices","ticker")
db.disconnect()