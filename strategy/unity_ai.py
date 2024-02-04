from strategy.anaistrategy import AnAIStrategy
from database.adatabase import ADatabase
from processor.processor import Processor as processor
from xgboost import XGBRegressor
import pandas as pd

class UnityAI(AnAIStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)
        self.factors = ["stochastic_oscillator","macd","bollinger","coefficient_of_variance","rsi"]
    
    def overhead(self):
        return None

    def signal(self,overhead,ticker_prices):
        model = XGBRegressor()
        ticker_prices["lower"] = ticker_prices["adjclose"].rolling(100).min() 
        ticker_prices["upper"] = ticker_prices["adjclose"].rolling(100).max()
        ticker_prices["stochastic_oscillator"] = (ticker_prices["upper"] - ticker_prices["lower"]) / ticker_prices["adjclose"]
        ticker_prices["upper"] = ticker_prices["adjclose"].rolling(50).mean() 
        ticker_prices["lower"] = ticker_prices["adjclose"].rolling(100).mean()
        ticker_prices["macd"] = (ticker_prices["upper"] - ticker_prices["lower"]) / ticker_prices["adjclose"]
        ticker_prices["upper"] = ticker_prices["adjclose"].rolling(100).mean() + 2 * ticker_prices["adjclose"].rolling(100).std()
        ticker_prices["bollinger"] = (ticker_prices["upper"] - ticker_prices["adjclose"]) / ticker_prices["adjclose"] 
        ticker_prices["coefficient_of_variance"] = ticker_prices["adjclose"].rolling(100).std() / ticker_prices["adjclose"].rolling(100).mean() 
        ticker_prices["rsi"] = ticker_prices["adjclose"].pct_change().rolling(100).mean() 
        ticker_prices["y"] = ticker_prices["adjclose"].pct_change(-5) 
        training_data = ticker_prices.iloc[:100].copy()
        simulation_data = ticker_prices.iloc[100:]
        model.fit(training_data[self.factors],training_data["y"])
        simulation_data[self.strategy.lower()] = model.predict(simulation_data[self.factors])
        simulation_data.dropna(inplace=True)
        return simulation_data