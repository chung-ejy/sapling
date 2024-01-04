from strategy.astrategy import AStrategy
class RSI(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def signal(self,ticker_prices):
        ticker_prices["signal"] = ticker_prices["adjclose"].pct_change().rolling(100).mean() 
        return ticker_prices