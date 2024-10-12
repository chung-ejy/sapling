
class Stock(object):

    def __init__(self,ticker="",adjclose=0,quantity=0):
        self.ticker = ticker
        self.adjclose = adjclose
        self.quantity = quantity

    def update(self,row):
        if float(row["adjclose"]) > self.adjclose * 1.2:
            self.adjclose = self.adjclose
        else:
            self.adjclose = float(row["adjclose"])
        self.date = row["date"]
        self.pv = self.adjclose * self.quantity
    
    def buy(self,row,notional):
        self.ticker = str(row["ticker"])
        self.date = row["date"]
        self.adjclose = float(row["adjclose"])
        self.buy_price = float(row["adjclose"])
        self.buy_date = row["date"]
        self.quantity = notional / self.adjclose
        self.pv = self.adjclose * self.quantity