from extractor.pandas_extractor import PandasExtractor as pex
import pandas as pd
from datetime import datetime, timedelta
from transformer.transformer import Transformer
from strategy.strategy_factory import StrategyFactory as stratfact
from parameter.aparameter import AParameter
from backtester.backtester import Backtester
import matplotlib.pyplot as plt 

param = AParameter()
strat = stratfact.build(param)
kospi = pd.read_excel("kospi.xlsx").rename(columns={"Ticker":"ticker"})
strat.tickers = kospi["ticker"]
start = datetime.now() - timedelta(days=365.25*20)
end = datetime.now()
simulation = Transformer.kospi_transform(strat,start,end)
trades = Backtester.backtest(strat,simulation)
portfolio = Backtester.portfolio(trades)
kpi = Backtester.kpi(trades,portfolio)
trades.to_csv("trades.csv")
portfolio.to_csv("portfolio.csv")
print(kpi)
plt.plot(portfolio["date"].values,portfolio["cumulative_return"].values)
plt.show()