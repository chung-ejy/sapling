from database.adatabase import ADatabase
from portfolio.portfolio import Portfolio
from backtester.backtester import Backtester
from strategy.single_index_quarterly import SingleIndexQuarterly
from strategy.magnificent_seven_quarterly import MagnificentSevenQuarterly
from strategy.financial_statement_quarterly import FinancialStatementQuarterly
from strategy.kr_financial_statement_yearly import KRFinancialStatementYearly
from strategy.korean_tech_quarterly import KoreanTechQuarterly
from strategy.optimal_quarterly import OptimalQuarterly
from diversifier.industry_diversifier import IndustryDiversifier
from diversifier.base_diversifier import BaseDiversifier
from diversifier.optimal_diversifier import OptimalDiversifier
from datetime import datetime, timedelta 
import pandas as pd

end = datetime.now()
start = datetime(2022,1,1)
market = ADatabase("market")
fred = ADatabase("fred")
sapling = ADatabase("sapling")

diversifier = BaseDiversifier()
strategies = [
            KRFinancialStatementYearly()
              # ,KoreanTechQuarterly()
              # ,OptimalQuarterly()
              # ,SingleIndexQuarterly()
              # ,MagnificentSevenQuarterly()
              # ,FinancialStatementQuarterly()
 
              ]

for strategy in strategies:
    sim = strategy.get_sim().sort_values("date")
    portfolio = Portfolio(strategy,diversifier,start,1000000,10)
    backtester = Backtester(portfolio,start,end)
    portfolio_dictionaries, trades = backtester.backtest(sim)
    states = pd.DataFrame(portfolio_dictionaries)
    strategy.db.connect()
    strategy.db.drop("states")
    strategy.db.store("states",states)
    strategy.db.drop("trades")
    strategy.db.store("trades",pd.DataFrame(trades))
    strategy.db.disconnect()