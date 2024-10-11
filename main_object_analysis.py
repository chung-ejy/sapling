from strategy.magnificent_seven_quarterly import MagnificentSevenQuarterly
from processor.processor import Processor as processor
from database.adatabase import ADatabase
import numpy as np

db = ADatabase("sapling")
fred = ADatabase("fred")
fred.connect()

market_yield = fred.retrieve("market_yield")
market_yield = market_yield.rename(columns={"value":"rf"})
market_yield["rf"] = market_yield["rf"].replace(".",np.nan)
market_yield.dropna(inplace=True)
market_yield["rf"] = [float(x)/100 for x in market_yield["rf"]]
market_yield = processor.column_date_processing(market_yield)
spy = fred.retrieve("sp500")
spy = spy.rename(columns={"value":"spy"})
spy["spy"] = spy["spy"].replace(".",np.nan)
spy.dropna(inplace=True)
spy["spy"] = [float(x) for x in spy["spy"]]
spy = processor.column_date_processing(spy)
spy = spy.sort_values("date")
fred.disconnect()
strategy = MagnificentSevenQuarterly()
strategy.db.connect()
states = strategy.db.retrieve("states")
trades = strategy.db.retrieve("trades")
strategy.db.disconnect()
visualization = states.merge(spy,on="date",how="left")
visualization = visualization.merge(market_yield[["date","rf"]],on="date",how="left")
visualization["return"] = (visualization["pv"] - visualization["pv"].iloc[0]) / visualization["pv"].iloc[0]
visualization["benchmark_return"] = (visualization["spy"] - visualization["spy"].iloc[0]) / visualization["spy"].iloc[0]
visualization["ir_return"] = (visualization["rf"] - visualization["rf"].iloc[0]) / visualization["rf"].iloc[0]

db.cloud_connect()
db.drop("visualization")
db.drop("trades")
db.store("visualization",visualization)
db.store("trades",trades)
db.disconnect()