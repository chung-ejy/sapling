from metric.ametric import AMetric
import pandas as pd

class RSI(AMetric):

    def __init__(self):
        super().__init__("rsi")
        self.ascending =  True
        self.positions = 10
        self.holding_period = 6
    
    def create_metric(self,price:pd.DataFrame):
        delta = price["adjclose"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        price["rsi"] = 100 - (100 / (1 + rs))
        return price
