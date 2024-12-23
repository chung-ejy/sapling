from datetime import datetime
from asset.exposure import Exposure
from data.market_data import MarketData
from copy import deepcopy
class Stock(object):

    def __init__(self
                ,ticker="" 
                ,sector="" 
                ,adjclose=0.0 
                ,quantity=0.0 
                ,purchase_date=datetime.now() 
                ,exposure=Exposure.LONG):
        self.ticker = ticker
        self.sector = sector
        self.adjclose = adjclose
        self.purchase_price = adjclose
        self.quantity = quantity
        self.purchase_date = purchase_date
        self.date = purchase_date
        self.exposure = exposure
        self.book_value = self.purchase_price * self.quantity

    def update(self,market_data : MarketData):
        self.date = market_data.date
        self.adjclose = market_data.adjclose
        if self.exposure == Exposure.LONG:
            self.book_value = self.quantity * self.adjclose
        elif self.exposure == Exposure.SHORT:
            self.book_value = self.quantity * (self.purchase_price + (self.purchase_price - self.adjclose))
        else:
            self.book_value = 0
            
    def buy(self,market_data:MarketData,notional):
        self.ticker = market_data.ticker
        self.date = market_data.date
        self.adjclose = market_data.adjclose
        self.purchase_date = market_data.date
        self.purchase_price = market_data.adjclose
        self.quantity = float(notional/self.adjclose)
        self.book_value = self.purchase_price * self.quantity
        self.exposure = market_data.exposure
    
    def sell(self):
        if self.exposure == Exposure.LONG:
            return self.quantity * self.adjclose
        elif self.exposure == Exposure.SHORT:
            return self.quantity * (self.purchase_price + (self.purchase_price - self.adjclose))
        else:
            return 0
    
    def to_json(self):
        result = deepcopy(self.__dict__)
        result["exposure"] = result["exposure"].value
        return result