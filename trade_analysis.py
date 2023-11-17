import pandas as pd
import matplotlib.pyplot as plt
from database.adatabase import ADatabase

market = ADatabase("market")
market.connect()
sp100 = market.retrieve("sp100").rename(columns={"Symbol":"ticker"})
market.disconnect()
trades = pd.read_csv("trades.csv").merge(sp100,on=["ticker"])
print(sp100)

plt.scatter(trades["std"].values,trades["return"].values)
plt.show()
print(trades[["GICS Sector","return"]].groupby("GICS Sector").mean())
print(trades[["ticker","return"]].groupby("ticker").mean().sort_values("return",ascending=False))