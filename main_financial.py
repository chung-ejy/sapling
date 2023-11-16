from database.adatabase import ADatabase
import pandas as pd
from processor.processor import Processor as p
from tqdm import tqdm

market = ADatabase("market")
market.connect()
sp100 = market.retrieve("sp100")
market.disconnect()

sp100 = sp100[:10]
market.connect()
factors = ["assets","liabilities","stockholdersequity"]
filings_data = []
for row in tqdm(sp100.iterrows()):
    try:
        ticker = row[1]["ticker"]
        cik = row[1]["cik"]
        prices = p.column_date_processing(market.query("prices",{"ticker":ticker}))
        filings = market.query("filings",{"cik":cik})
        data = p.merge(prices,filings,["year","quarter"])
        data = data.drop(["date","cik"],axis=1)[["year","quarter","ticker","assets","liabilities","stockholdersequity","adjclose"]].groupby(["year","quarter","ticker"]).mean().reset_index()
        data.sort_values(["year","quarter"],inplace=True)
        data["y"] = data["adjclose"].shift(-4)
        filings_data.append(data)
    except Exception as e:
        print(str(e))
market.disconnect()

model_data = pd.concat(filings_data)
print(model_data)