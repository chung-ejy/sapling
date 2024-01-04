from strategy.astrategy import AStrategy
class AverageReturn(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def signal(self,ticker_prices):
        ticker_prices["signal"] = (ticker_prices["adjclose"] - ticker_prices["adjclose"].shift(self.holding_period)) / ticker_prices["adjclose"].shift(self.holding_period) 
        ticker_prices["signal"] = ticker_prices["signal"].rolling(self.holding_period*10).mean()
        return ticker_prices