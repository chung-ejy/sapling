from strategy.astrategy import AStrategy
class MovingAverage(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def signal(self,ticker_prices):
        ticker_prices["signal"] = (ticker_prices["adjclose"] - ticker_prices["adjclose"].rolling(self.holding_period).mean()) / ticker_prices["adjclose"].rolling(self.holding_period).mean() 
        return ticker_prices