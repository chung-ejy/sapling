from datetime import datetime
from asset.stock import Stock
from asset.option import Option
from asset.bond import Bond
class Portfolio(object):
    
    def __init__(self,strategy,diversifier,date=datetime(datetime.now().year,1,1),cash=100000,number_of_positions=50):
        self.strategy = strategy
        self.diversifier = diversifier
        self.date = date
        self.initial_pv = cash
        self.cash = cash
        self.pv = cash
        self.portfolio_return = (self.pv - self.initial_pv) / self.initial_pv
        self.number_of_positions = number_of_positions
        self.stocks = []
        self.options = []
        self.bonds = []
        self.asset_allocations = {"stock":0.6,"option":0,"bond":0.4}
    
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
            option = [x for x in self.options if x.ticker == ticker][0]
            bond = [x for x in self.bonds if x.ticker == ticker][0]
            option.update(row)
            bond.update(row)
        self.stock_pv = sum([stock.adjclose * stock.quantity for stock in self.stocks])
        self.option_pv = sum([option.pv for option in self.options])
        self.bond_pv = sum([bond.pv for bond in self.bonds])
        self.pv = self.stock_pv + self.option_pv + self.bond_pv + self.cash
        self.portfolio_return = (self.pv - self.initial_pv) / self.initial_pv

    def buy(self,todays_sim):
        cash = float(self.cash)
        if len(self.stocks) == 0:
            for i in range(self.number_of_positions):
                diversified_sim = self.diversifier.diversify(todays_sim,i,self.number_of_positions)
                if diversified_sim.index.size < 1:
                    row = todays_sim.sort_values(self.strategy.metric, ascending=self.strategy.growth).iloc[i]
                else:
                    row = diversified_sim.sort_values(self.strategy.metric, ascending=self.strategy.growth).iloc[i]
                stock = Stock()
                option = Option()
                bond = Bond()
                notional = cash * row["weight"]
                stock.buy(row, notional*self.asset_allocations["stock"])
                self.add_stock(stock)
                self.withdraw(stock.pv)
                option.buy(row,notional*self.asset_allocations["option"])
                self.options.append(option)
                self.withdraw(option.pv)
                bond.buy(row,notional*self.asset_allocations["bond"])
                self.bonds.append(bond)
                self.withdraw(bond.pv)

    def sell(self,todays_sim):
        trades = []
        for stock in self.stocks:
            if self.strategy.sell_clause(self.date,stock):
                self.remove_stock(stock)
                option = [x for x in self.options if x.ticker == stock.ticker][0]
                self.options.remove(option)
                bond = [x for x in self.bonds if x.ticker == stock.ticker][0]
                self.bonds.remove(bond)
                trades.append(stock.__dict__)
                self.deposit(stock.pv)
                self.deposit(option.pv)
                self.deposit(bond.pv)   
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