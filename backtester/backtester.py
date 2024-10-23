from datetime import datetime
from tqdm import tqdm
import copy
from portfolio.portfolio import Portfolio

class Backtester(object):

    def __init__(self,portfolio: Portfolio,start_date=datetime(datetime.now().year,1,1),end_date=datetime.now()):
        self.start_date = start_date
        self.end_date = end_date
        self.portfolio = portfolio

    def backtest(self,sim):
        portfolio_dictionaries = []
        trades = []
        sim = sim[(sim["date"]>self.start_date) & (sim["date"]<self.end_date)]
        for date in tqdm(sim["date"].unique()):      
            try:
                today = sim[sim["date"] == date].copy()
                if today.index.size > self.portfolio.number_of_positions:
                    self.portfolio.update(today)
                    trades.extend(self.portfolio.sell(today))
                    self.portfolio.buy(today)
                    portfolio_dictionaries.append(self.portfolio.to_json())
            except Exception as e:
                print(f"Error on date {date}: {str(e)}")
                continue
        return portfolio_dictionaries, trades
