from data.core_data import CoreData
from strategy.coev_weekly import COEVWeekly
from strategy.rolling_average_quarterly import RollingAverageQuarterly
from strategy.rolling_average_weekly import RollingAverageWeekly
from strategy.magnificent_seven_quarterly import MagnificentSevenQuarterly
from equations.date_columns import DateColumns
from data.market_data import MarketData
from portfolio.portfolio import Portfolio
from backtester.backtester import Backtester
from datetime import datetime
import pandas as pd

core_data = CoreData()
core_data.load_index()
standard_market = core_data.core_dataframe()
strategy = COEVWeekly()
strategy.load_index()
sim = strategy.factor_load(standard_market)
sim = DateColumns.apply(sim)
sim = strategy.signal(sim)
market_data_list = [MarketData.build(row[1]) for row in sim.iterrows()]
portfolio = Portfolio(strategy,datetime(2020,1,1),100)
backtester = Backtester(portfolio,datetime(2020,1,1))
states = backtester.backtest(market_data_list)

strategy.db.connect()
strategy.db.drop("states")
strategy.db.store("states",pd.DataFrame(states))
strategy.db.disconnect()