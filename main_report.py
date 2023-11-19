from algo.algo import Algo
from database.adatabase import ADatabase
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from random import shuffle
db = ADatabase("algo")
tickers = pd.read_csv("tickers.csv")["ticker"]

skip = 1
queries = []
rrs = [0,0.1,0.2,0.3]
rolling_vals = [10,20,50,100]
projection_weeks = [1,2,4,13,26]
shuffle(rrs)
shuffle(rolling_vals)
shuffle(projection_weeks)
rr = rrs[0]
risk = rrs[-1]
rolling_val = rolling_vals[0]
projection_week = projection_weeks[0]
trades = Algo(rolling_val,projection_week,rr,risk,tickers,skip).algo()
trades["avg_risk"] = trades["risk"].mean()
plt.plot(trades["date"].values,trades["cr"].values)
plt.show()
report = trades.tail(1).to_dict("records")[0]
print(report)