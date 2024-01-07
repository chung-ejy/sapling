
class AStrategy(object):

    def __init__(self,parameter):
        for key in parameter.__dict__.keys():
            self.__setattr__(key,parameter.__dict__[key])

    def overhead(self):
        return None
    
    def signal(self,overhead,ticker_prices):
        ticker_prices[self.strategy.lower()] = ticker_prices["adjclose"]
        return ticker_prices