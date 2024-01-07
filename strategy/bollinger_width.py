from strategy.astrategy import AStrategy

class BollingerWidth(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def signal(self,overhead,ticker_prices):
        ticker_prices["upper"] = ticker_prices["adjclose"].rolling(self.holding_period).mean() + 2 * ticker_prices["adjclose"].rolling(self.holding_period).std()
        ticker_prices["lower"] = ticker_prices["adjclose"].rolling(self.holding_period).mean() - 2 * ticker_prices["adjclose"].rolling(self.holding_period).std()
        ticker_prices[self.strategy.lower()] = (ticker_prices["upper"] - ticker_prices["lower"]) / ticker_prices["adjclose"] 
        return ticker_prices