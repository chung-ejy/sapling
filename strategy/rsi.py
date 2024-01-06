from strategy.astrategy import AStrategy
class RSI(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def signal(self,overhead,ticker_prices):
        ticker_prices[self.strategy.lower()] = ticker_prices["adjclose"].pct_change().rolling(100).mean() 
        return ticker_prices