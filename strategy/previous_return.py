from strategy.astrategy import AStrategy
import pandas as pd
from parameter.aparameter import AParameter

class PreviousReturn(AStrategy):

    def __init__(self,parameters: AParameter):
        super().__init__("previous_return",parameters)
        self.ascending = True
    
    def create_signal(self,price:pd.DataFrame):
        price["signal"] = price["adjclose"].pct_change(5)
        return price