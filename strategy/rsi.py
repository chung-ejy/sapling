
class RSI(object):

    def __init__(self,parameter):
        for key in parameter.__dict__.keys():
            self.__setattr__(key,parameter.__dict__[key])

    def signal(self,ticker_prices):
        ticker_prices["signal"] = ticker_prices["adjclose"].pct_change().rolling(100).mean() 
        return ticker_prices