from database.adatabase import ADatabase
from asset.exposure import Exposure
from asset.stock import Stock

class AStrategy(object):

    def __init__(self,name,index):
        self.name = name
        self.db = ADatabase(self.name)
        self.market = ADatabase("market")
        self.sec = ADatabase("sec")
        self.fred = ADatabase("fred")
        self.index = index

    def load_index(self):
        self.market.connect()
        self.index = self.market.retrieve(self.index)
        self.market.disconnect()
        self.tickers = list(self.index["ticker"].unique())
    
    def buy_clause(self,market_data):
        return market_data.exposure != Exposure.NONE
    
    def buy(self,market_data,notional):
        asset = Stock()
        asset.buy(market_data,notional)
        return asset
    
    def sell(self,asset):
        return asset.sell()
    
    def update(self,asset,market_data):
        asset.update(market_data)
        