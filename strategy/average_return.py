from strategy.astrategy import AStrategy
class AverageReturn(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def signal(self,overhead,ticker_prices):
        ticker_prices[self.strategy.lower()] = (ticker_prices["adjclose"] - ticker_prices["adjclose"].shift(self.holding_period)) / ticker_prices["adjclose"].shift(self.holding_period) 
        ticker_prices[self.strategy.lower()] = ticker_prices[self.strategy.lower()].rolling(self.holding_period*10).mean()
        return ticker_prices