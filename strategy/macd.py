from strategy.astrategy import AStrategy
class MACD(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def signal(self,overhead,ticker_prices):
        ticker_prices["upper"] = ticker_prices["adjclose"].rolling(50).mean() 
        ticker_prices["lower"] = ticker_prices["adjclose"].rolling(100).mean()
        ticker_prices[self.strategy.lower()] = (ticker_prices["upper"] - ticker_prices["lower"]) / ticker_prices["adjclose"] 
        return ticker_prices