from strategy.astrategy import AStrategy
class MovingAverage(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def signal(self,overhead,ticker_prices):
        ticker_prices[self.strategy.lower()] = (ticker_prices["adjclose"] - ticker_prices["adjclose"].rolling(self.holding_period).mean()) / ticker_prices["adjclose"].rolling(self.holding_period).mean() 
        return ticker_prices