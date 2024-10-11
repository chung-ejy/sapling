
class Stock(object):

    def __init__(self,ticker="",adjclose=0,quantity=0):
        self.ticker = ticker
        self.adjclose = adjclose
        self.quantity = quantity

    def update(self,row):
        self.adjclose = row["adjclose"]
        self.date = row["date"]
        self.pv = self.adjclose * self.quantity
    
    def buy(self,row,notional):
        self.ticker = row["ticker"]
        self.date = row["date"]
        self.adjclose = row["adjclose"]
        self.buy_price = row["adjclose"]
        self.buy_date = row["date"]
        self.quantity = notional / self.adjclose
        self.pv = self.adjclose * self.quantity