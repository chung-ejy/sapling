from strategy.anaistrategy import AnAIStrategy
from database.adatabase import ADatabase
from processor.processor import Processor as processor
from xgboost import XGBRegressor
import pandas as pd

class Technical(AnAIStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)
        self.factors = [str(i) for i in range(10)]
    
    def overhead(self):
        return None

    def signal(self,overhead,ticker_prices):
        model = XGBRegressor()
        for i in range(10):
            ticker_prices[str(i)] = ticker_prices["adjclose"].shift(i)
        ticker_prices["y"] = ticker_prices["adjclose"].pct_change(-5) 
        training_data = ticker_prices.iloc[:100].copy()
        simulation_data = ticker_prices.iloc[100:]
        model.fit(training_data[self.factors],training_data["y"])
        simulation_data["signal"] = model.predict(simulation_data[self.factors])
        simulation_data.dropna(inplace=True)
        return simulation_data