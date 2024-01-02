
class Skew(object):

    def __init__(self,parameter):
        for key in parameter.__dict__.keys():
            self.__setattr__(key,parameter.__dict__[key])

    def signal(self,ticker_prices):
        ticker_prices["signal"] = (ticker_prices["adjclose"] - ticker_prices["adjclose"].shift(self.holding_period)) / ticker_prices["adjclose"].shift(self.holding_period) 
        ticker_prices["signal"] = ticker_prices["signal"].rolling(self.holding_period*10).skew()
        return ticker_prices