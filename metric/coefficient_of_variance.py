from metric.ametric import AMetric
import pandas as pd

class CoefficientOfVariance(AMetric):

    def __init__(self):
        super().__init__("coefficient_of_variance")
        self.ascending =  False
        self.positions = 10
        self.holding_period = 4
    
    def create_metric(self,price:pd.DataFrame):
        price[self.name] = price["adjclose"].rolling(100).std() / price["adjclose"].rolling(100).mean()
        return price