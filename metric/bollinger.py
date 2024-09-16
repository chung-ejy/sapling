from metric.ametric import AMetric
import pandas as pd

class Bollinger(AMetric):

    def __init__(self):
        super().__init__("bollinger")
        self.ascending =  True
        self.positions = 10
        self.holding_period = 6
    
    def create_metric(self,price:pd.DataFrame):
        price["bollinger"] = ((price["adjclose"].rolling(100).mean() - 2 * price["adjclose"].rolling(100).std()) - price["adjclose"]) / price["adjclose"]
        return price