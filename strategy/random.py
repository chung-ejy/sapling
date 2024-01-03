import random

class Random(object):

    def __init__(self,parameter):
        for key in parameter.__dict__.keys():
            self.__setattr__(key,parameter.__dict__[key])

    def signal(self,ticker_prices):
        ticker_prices["signal"] = [random.randint(0,1009) for x in range(ticker_prices.index.size)]
        return ticker_prices