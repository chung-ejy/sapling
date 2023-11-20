from strategy.astrategy import AStrategy
class Technical(AStrategy):

    def __init__(self):
        super().__init__("technical")
        self.factors = [str(i) for i in range(10)]
        self.isai = True
        
    def transform(self,ticker):
        prices = super().transform(ticker)
        prices.sort_values("date",inplace=True)
        for i in range(10):
            prices[str(i)] = prices["adjclose"].shift(i)
        prices["y"] = prices["adjclose"].shift(-5)
        return prices
    
    
    #model
    #signals
    #cfasignals
    #returns
    #backtest_filter