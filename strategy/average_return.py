from strategy.astrategy import AStrategy
import pandas as pd
from parameter.aparameter import AParameter

class AverageReturn(AStrategy):

    def __init__(self,parameters: AParameter):
        super().__init__("average_return",parameters)
        self.ascending = True
    
    def create_signal(self,price:pd.DataFrame):
        price["signal"] = price["adjclose"].pct_change(5).rolling(100).mean()
        return price