from metric.ametric import AMetric
import pandas as pd

class PreviousReturn(AMetric):

    def __init__(self):
        super().__init__("previous_return")
        self.ascending =  True
        self.positions = 1
        self.holding_period = 6
    
    def create_metric(self,price:pd.DataFrame):
        price[self.name] = price["adjclose"].pct_change(5)
        return price