import random
from strategy.astrategy import AStrategy
class Random(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)

    def signal(self,overhead,ticker_prices):
        ticker_prices[self.strategy.lower()] = [random.randint(0,1009) for x in range(ticker_prices.index.size)]
        return ticker_prices