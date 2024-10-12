from datetime import datetime
from asset.stock import Stock
import copy
class Portfolio(object):
    
    def __init__(self,strategy,date=datetime(datetime.now().year,1,1),cash=100000,number_of_positions=50):
        self.strategy = strategy
        self.date = date
        self.initial_pv = cash
        self.cash = cash
        self.pv = cash
        self.portfolio_return = (self.pv - self.initial_pv) / self.initial_pv
        self.number_of_positions = number_of_positions
        self.stocks = []
    
    def update_date(self,date):
        self.date = date

    def deposit(self,amount):
        self.cash += amount

    def withdraw(self,amount):
        self.cash += -amount

    def add_stock(self,stock):
        self.stocks.append(stock)
    
    def remove_stock(self,stock):
        self.stocks.remove(stock)
 
    def update(self,todays_sim):
        self.date = todays_sim["date"].iloc[0]
        for stock in self.stocks:
            ticker = stock.ticker
            row = todays_sim[todays_sim["ticker"] == ticker].iloc[0]
            stock.update(row)
        self.pv = sum([stock.adjclose * stock.quantity for stock in self.stocks]) + self.cash
        self.portfolio_return = (self.pv - self.initial_pv) / self.initial_pv

    def buy(self,todays_sim):
        notional = float(self.cash / self.number_of_positions)
        if len(self.stocks) == 0:
            for i in range(self.number_of_positions):
                row = todays_sim.sort_values(self.strategy.metric, ascending=self.strategy.growth).iloc[i]
                stock = Stock()
                stock.buy(row, notional)
                self.add_stock(stock)
                self.withdraw(stock.pv)

    def sell(self,todays_sim):
        trades = []
        for stock in self.stocks:
            if self.strategy.sell_clause(self.date,stock):
                self.remove_stock(stock)
                trades.append(stock.__dict__)
                self.deposit(stock.pv)
        return trades
    
    def to_json(self):
        result = {
            "date":self.date,
            "cash":self.cash,
            "pv":self.pv,
            "portfolio_return":self.portfolio_return,
            "stocks":[stock.__dict__.copy() for stock in self.stocks]
        }
        return result