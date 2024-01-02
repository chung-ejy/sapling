
class StandardDeviation(object):

    def __init__(self,parameter):
        for key in parameter.__dict__.keys():
            self.__setattr__(key,parameter.__dict__[key])

    def signal(self,ticker_prices):
        ticker_prices["signal"] = ticker_prices["adjclose"].rolling(self.holding_period*10).std()
        return ticker_prices