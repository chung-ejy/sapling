from extractor.open_dart_extractor import OpenDartExtractor
from database.adatabase import ADatabase
import pandas as pd
from tqdm import tqdm
import warnings
warnings.simplefilter(action="ignore")
db = ADatabase("open_dart")
db.connect()
companies = db.retrieve("companies")
db.disconnect()
companies["stock_code"] = [x.strip().zfill(6) for x in companies["stock_code"]]
companies["corp_code"] = [str(x).strip().zfill(8) for x in companies["corp_code"]]
companies_with_stocks = companies[companies["stock_code"] != ""]
companies_with_stocks.rename(columns={"stock_code":"ticker"},inplace=True)
kospi = pd.read_csv("kospi.csv").rename(columns={"Issue code":"ticker"})
kospi["ticker"] = [str(x).zfill(6) for x in kospi["ticker"]]
kospi = kospi.merge(companies_with_stocks,on="ticker",how="left")
db.connect()
db.drop("kospi")
db.store("kospi",kospi)
db.disconnect()
print(kospi)
db.connect()
db.drop("filings")
for corp_code in tqdm(list(kospi["corp_code"].unique())):
    for year in range(2015,2024):
        try:
            filing = OpenDartExtractor.filing(corp_code,year)
            filing = pd.DataFrame(filing["list"])
            filings = filing[["stock_code","account_nm","thstrm_amount"]]
            filings["account_nm"] = [x.strip() for x in filings["account_nm"]]
            filings["thstrm_amount"] = [int(x.replace(",","")) / 1000 for x in filings["thstrm_amount"]]
            filings = filings.pivot_table(index="stock_code",columns="account_nm",values="thstrm_amount").reset_index().rename(columns={"stock_code":"ticker"})
            filings["year"] = year
            db.store("filings",filings)
        except:
            print(corp_code,year,"no filing")
db.disconnect()