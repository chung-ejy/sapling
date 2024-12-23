from database.adatabase import ADatabase
from processor.processor import Processor as processor
from strategy.astrategy import AStrategy
import numpy as np
from xgboost import XGBRegressor
class AnAIStrategy(AStrategy):

    def __init__(self,name,index,factors):
        super().__init__(name,index)
        self.factors = factors
    
    def model(self,training_data,price):
        model = XGBRegressor()
        model.fit(training_data[self.factors],training_data["y"])
        price["prediction"] = model.predict(price[self.factors])
        return price