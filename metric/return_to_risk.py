from metric.ametric import AMetric
import pandas as pd

class ReturnToRisk(AMetric):

    def __init__(self):
        super().__init__("return_to_risk")
        self.ascending =  True
        self.positions = 10
        self.holding_period = 6
    
    def create_metric(self,price:pd.DataFrame):
        price["prev_return"] = price["adjclose"].pct_change(5)
        price["coev"] = price["adjclose"].rolling(100).std() / price["adjclose"].rolling(100).mean()
        price["return_to_risk"] = price["prev_return"] / price["coev"]
        return price