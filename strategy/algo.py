from strategy.astrategy import AStrategy

class Algo(AStrategy):

    def __init__(self):
        super().__init__("algo")
        self.isai = False

    def transform(self,ticker):
        prices = super().transform(ticker)
        prices["prediction"] = prices["adjclose"].rolling(self.parameter.holding_period*2).mean()
        return prices