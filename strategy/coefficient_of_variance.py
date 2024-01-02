from datetime import timedelta

class CoefficientOfVariance(object):

    def __init__(self,parameter):
        for key in parameter.__dict__.keys():
            self.__setattr__(key,parameter.__dict__[key])

    def signal(self,ticker_prices):
        ticker_prices["signal"] = ticker_prices["adjclose"].rolling(self.holding_period*10).std() / ticker_prices["adjclose"].rolling(self.holding_period*10).mean()
        return ticker_prices