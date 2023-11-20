from strategy.astrategy import AStrategy

class Metrics(AStrategy):

    def __init__(self):
        super().__init__("metrics")
        self.isai = True
        self.factors = ["upper","lower","max","rsi"]

    def transform(self,ticker):
        prices = super().transform(ticker)
        prices["lower"] = prices["adjclose"].rolling(self.parameter.holding_period).mean() - prices["adjclose"].rolling(self.parameter.holding_period).std()
        prices["upper"] = prices["adjclose"].rolling(self.parameter.holding_period).mean() + prices["adjclose"].rolling(self.parameter.holding_period).std()
        prices["max"] =  prices["adjclose"].rolling(self.parameter.holding_period).max()
        prices["rsi"] =  prices["adjclose"].pct_change().rolling(self.parameter.holding_period).mean()
        prices["y"] = prices["adjclose"].shift(-self.parameter.holding_period)
        return prices