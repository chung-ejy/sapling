from database.adatabase import ADatabase
from portfolio.portfolio import Portfolio
from backtester.backtester import Backtester
from strategy.single_index_weekly import SingleIndexWeekly
from strategy.magnificent_seven_quarterly import MagnificentSevenQuarterly
from strategy.coefficient_of_variance import CoefficientOfVariance
from strategy.financial_statement_quarterly import FinancialStatementQuarterly
from strategy.korean_tech_quarterly import KoreanTechQuarterly
from datetime import datetime, timedelta 
import pandas as pd


end = datetime.now()
start = datetime.now() - timedelta(days=365.25*2)

strategy = KoreanTechQuarterly()
market = ADatabase("market")
fred = ADatabase("fred")
sapling = ADatabase("sapling")


sim = strategy.get_sim()
portfolio = Portfolio(strategy,start,100000,10)
backtester = Backtester(portfolio,start,end)
portfolio_dictionaries, trades = backtester.backtest(sim)
states = pd.DataFrame(portfolio_dictionaries)
strategy.db.connect()
strategy.db.drop("states")
strategy.db.store("states",states)
strategy.db.drop("trades")
strategy.db.store("trades",pd.DataFrame(trades))
strategy.db.disconnect()