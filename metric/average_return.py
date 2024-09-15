from metric.ametric import AMetric
import pandas as pd

class AverageReturn(AMetric):

    def __init__(self):
        super().__init__("average_return")
        self.ascending =  False
        self.positions = 10
        self.holding_period = 6
    
    def create_metric(self,price:pd.DataFrame):
        price[self.name] = price["adjclose"].pct_change(5).rolling(100).mean()
        return price