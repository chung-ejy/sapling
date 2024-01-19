from strategy.astrategy import AStrategy

class RSIToCoev(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def signal(self,overhead,ticker_prices):
        ticker_prices["coev"] = ticker_prices["adjclose"].rolling(100).std() / ticker_prices["adjclose"].rolling(100).mean()
        ticker_prices["rsi"] = ticker_prices["adjclose"].pct_change().rolling(100).mean() 
        ticker_prices[self.strategy.lower()] = ticker_prices["rsi"] / ticker_prices["coev"] 
        return ticker_prices