from strategy.astrategy import AStrategy
class StandardDeviation(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def signal(self,overhead,ticker_prices):
        ticker_prices[self.strategy.lower()] = ticker_prices["adjclose"].rolling(self.holding_period*10).std()
        return ticker_prices