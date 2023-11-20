from strategy.astrategy import AStrategy

class Rolling(AStrategy):

    def __init__(self):
        super().__init__("rolling")
        self.isai = True
        self.factors = ["rolling_20","rolling_50","rolling_100"]

    def transform(self,ticker):
        prices = super().transform(ticker)
        prices["rolling_20"] = prices["adjclose"].rolling(20).mean()
        prices["rolling_50"] = prices["adjclose"].rolling(50).mean()
        prices["rolling_100"] = prices["adjclose"].rolling(100).mean()
        prices["y"] = prices["adjclose"].shift(-self.parameter.holding_period)
        return prices