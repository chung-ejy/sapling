from strategy.astrategy import AStrategy

class Bollinger(AStrategy):

    def __init__(self):
        super().__init__("bollinger")
        self.isai = True
        self.factors = ["upper","lower"]

    def transform(self,ticker):
        prices = super().transform(ticker)
        prices["lower"] = prices["adjclose"].rolling(self.parameter.holding_period).mean() - prices["adjclose"].rolling(self.parameter.holding_period).std()
        prices["upper"] = prices["adjclose"].rolling(self.parameter.holding_period).mean() + prices["adjclose"].rolling(self.parameter.holding_period).std() 
        prices["y"] = prices["adjclose"].shift(-self.parameter.holding_period)
        return prices