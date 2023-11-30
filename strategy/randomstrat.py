from strategy.astrategy import AStrategy
import random
class RandomStrat(AStrategy):

    def __init__(self):
        super().__init__("rolling")
        self.isai = True
        self.factors = ["col1","col2","col3"]

    def transform(self,ticker):
        prices = super().transform(ticker)
        prices["co1"] = prices["adjclose"].rolling(random.randint(0,100)).mean()
        prices["col2"] = prices["adjclose"].rolling(random.randint(0,100)).mean()
        prices["col3"] = prices["adjclose"].rolling(random.randint(0,100)).mean()
        prices["y"] = prices["adjclose"].shift(-self.parameter.holding_period)
        return prices