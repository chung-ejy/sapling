from datetime import datetime
from tqdm import tqdm
from copy import deepcopy
from portfolio.portfolio import Portfolio
from data.market_data import MarketData
from asset.exposure import Exposure
class Backtester(object):

    def __init__(self,portfolio: Portfolio,start_date=datetime(datetime.now().year,1,1),end_date=datetime.now()):
        self.start_date = start_date
        self.end_date = end_date
        self.portfolio = portfolio

    def backtest(self,sim):
        portfolio_dictionaries = []
        sim = list(filter(lambda x: x.date > self.start_date and x.date < self.end_date,sim))
        dates = list(set(list(map(lambda x: x.date,sim))))
        dates.sort()
        for date in dates:      
            try:
                today = list(filter(lambda x: x.date == date,sim))
                self.portfolio.update(today)
                self.portfolio.sell(today)
                if self.portfolio.buy_clause():
                    self.portfolio.buy(today)
                portfolio_dictionaries.append(self.portfolio.to_json())
            except Exception as e:
                print(f"Error on date {date}: {str(e)}")
                continue
        return portfolio_dictionaries
