from database.adatabase import ADatabase
from processor.processor import Processor as processor
from datetime import datetime, timedelta
from tqdm import tqdm 
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from time import sleep
import numpy as np
import warnings
warnings.simplefilter(action="ignore")
from portfolio.portfolio import Portfolio
from backtester.backtester import Backtester
from strategy.single_index_weekly import SingleIndexWeekly
from strategy.magnificent_seven_quarterly import MagnificentSevenQuarterly
end = datetime.now()
start = datetime.now() - timedelta(days=365.25*2)


market = ADatabase("market")
fred = ADatabase("fred")
sapling = ADatabase("sapling")
strategy = MagnificentSevenQuarterly()

sim = strategy.get_sim()
portfolio = Portfolio(strategy,start,100000,10)
backtester = Backtester(portfolio,start,end)
portfolio_dictionaries, trades = backtester.backtest(sim)
states = pd.DataFrame(portfolio_dictionaries)
print(trades)
strategy.db.connect()
strategy.db.drop("states")
strategy.db.store("states",states)
strategy.db.drop("trades")
strategy.db.store("trades",pd.DataFrame(trades))
strategy.db.disconnect()