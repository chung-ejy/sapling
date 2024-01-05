from strategy.astrategy import AStrategy
from processor.processor import Processor as processor
from xgboost import XGBRegressor
import pandas as pd

class AnAIStrategy(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)
    
    def signal(self,overhead,ticker_prices):
        model = XGBRegressor()
        ticker_prices = processor.merge(ticker_prices,overhead,on="date")
        ticker_prices["historical_return"] = ticker_prices["adjclose"].pct_change(5)
        ticker_prices["y"] = ticker_prices["adjclose"].pct_change(-5) 
        training_data = ticker_prices.iloc[:100].copy()
        simulation_data = ticker_prices.iloc[100:]
        model.fit(training_data[self.factors],training_data["y"])
        simulation_data["signal"] = model.predict(simulation_data[self.factors])
        simulation_data.dropna(inplace=True)
        return simulation_data