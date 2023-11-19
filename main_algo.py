from algo.algo import Algo
from database.adatabase import ADatabase
import pandas as pd
from tqdm import tqdm

db = ADatabase("algo")
tickers = pd.read_csv("tickers.csv")["ticker"]

skip = 1
queries = []
rr = 0
risk = 1
for rolling_val in [10,20,60,100]:
    for projection_weeks in [51,1,2,4,13,26]:
        query = {
            "rr":rr,
            "risk":risk,
            "rolling_val":rolling_val,
            "projection_week":projection_weeks,
        }
        queries.append(query)
reports = []
print(len(queries))
db.connect()
db.drop("reports")
db.drop("trades")
for query in tqdm(queries):
    try:
        rr = query["rr"]
        risk = query["risk"]
        rolling_val = query["rolling_val"]
        projection_week = query["projection_week"]
        trades = Algo(rolling_val,projection_week,rr,risk,tickers,skip).algo()
        trades["avg_risk"] = trades["risk"].mean()
        for key in query.keys():
            trades[key] = query[key]
        db.store("trades",trades)
        report = trades.tail(1).to_dict("records")[0]
        report.update(query)
        report = pd.DataFrame([report])[["rr","avg_risk","risk","rolling_val","projection_week","cr"]]
        db.store("reports",report)
    except Exception as e:
        print(str(e))
db.disconnect()