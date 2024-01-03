
class StochasticOscillator(object):

    def __init__(self,parameter):
        for key in parameter.__dict__.keys():
            self.__setattr__(key,parameter.__dict__[key])

    def signal(self,ticker_prices):
        ticker_prices["upper"] = ticker_prices["adjclose"].rolling(self.holding_period).min() 
        ticker_prices["lower"] = ticker_prices["adjclose"].rolling(self.holding_period).max()
        ticker_prices["signal"] = (ticker_prices["upper"] - ticker_prices["lower"]) / ticker_prices["adjclose"] 
        return ticker_prices