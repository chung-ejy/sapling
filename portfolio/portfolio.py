from datetime import datetime
from asset.exposure import Exposure
class Portfolio(object):
    
    def __init__(self,strategy,date=datetime(datetime.now().year,1,1),cash=100):
        self.strategy = strategy
        self.date = date
        self.cash = cash
        self.assets = []
 
    def update(self,market_data):
        self.date = market_data[0].date
        for asset in self.assets:
            asset_data = list(filter(lambda x: x.ticker == asset.ticker,market_data))[0]
            self.strategy.update(asset,asset_data)

    def buy(self,market_data):
        buys =list(filter(lambda x: x.exposure != Exposure.NONE,market_data))
        notional = self.cash / len(buys)
        for buy in buys:
            asset_data = list(filter(lambda x: x.ticker == buy.ticker,market_data))[0]
            if self.strategy.buy_clause(asset_data):
                asset = self.strategy.buy(asset_data,notional)
                self.cash += -notional
                self.assets.append(asset)

    def sell(self,market_data):
        for asset in self.assets:
            asset_data = list(filter(lambda x: x.ticker == asset.ticker,market_data))[0]
            if self.strategy.sell_clause(asset,asset_data):
                self.cash += self.strategy.sell(asset)
                self.assets.remove(asset)
    
    def buy_clause(self):
        return len(self.assets) == 0 
    
    def to_json(self):
        return {
            "date":self.date,
            "cash":self.cash,
            "assets": [x.to_json() for x in self.assets]
        }