from database.adatabase import ADatabase
import pandas as pd
from processor.processor import Processor as p
from tqdm import tqdm
from xgboost import XGBRegressor

db = ADatabase("financial")
market = ADatabase("market")
market.connect()
sp100 = market.retrieve("sp100")
market.disconnect()

market.connect()
factors = ["totalassets","totalliabilities","totalstockholdersequity"]
filings_data = []
for row in tqdm(sp100.iterrows()):
    try:
        ticker = row[1]["ticker"]
        cik = row[1]["cik"]
        prices = p.column_date_processing(market.query("prices",{"ticker":ticker}))
        filings = p.column_date_processing(market.query("balance_sheet",{"symbol":ticker})).rename(columns={"symbol":"ticker"})
        data = p.merge(prices,filings,["year","quarter"])
        data = data.drop(["date","cik"],axis=1)[["year","ticker","totalassets","totalliabilities","totalstockholdersequity","adjclose"]]
        data = data.groupby(["year","ticker"]).mean().dropna().reset_index()
        data.sort_values(["year","quarter"],inplace=True)
        data["y"] = data["adjclose"].shift(-4)
        filings_data.append(data)
    except Exception as e:
        print(str(e))
market.disconnect()

model_data = pd.concat(filings_data)
training_data = model_data[model_data["year"]<2021].dropna().copy().reset_index()
recommendation_data = model_data[model_data["year"]>=2021].copy().reset_index()
model = XGBRegressor(booster="dart",learning_rate=0.5)
model.fit(training_data[factors],training_data["y"])
recommendation_data["prediction"] = model.predict(recommendation_data[factors])

## note the format of this db is year quarter prediction
db.connect()
db.drop("simulation")
db.store("simulation",recommendation_data[["year","quarter","ticker","prediction"]])
db.disconnect()