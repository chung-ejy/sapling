from algo.algo import Algo
from database.adatabase import ADatabase
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

db = ADatabase("algo")
tickers = pd.read_csv("tickers.csv")["ticker"]

skip = 1
queries = []
rr = 0.0
risk = 0.10
# rolling_val = 20
# projection_week = 13
rolling_val = 50
projection_week = 1
trades = Algo(rolling_val,projection_week,rr,risk,tickers,skip).algo()
trades["avg_risk"] = trades["risk"].mean()
plt.plot(trades["date"].values,trades["cr"].values)
plt.show()
report = trades.tail(1).to_dict("records")[0]
print(report)