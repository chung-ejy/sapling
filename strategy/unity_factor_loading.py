from strategy.afactorloadingstrategy import AFactorLoadingStrategy
from database.adatabase import ADatabase
from processor.processor import Processor as processor
import pandas as pd
from datetime import datetime, timedelta
from extractor.alp_extractor import ALPExtractor

class UnityFactorLoading(AFactorLoadingStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)
        self.factors = ["stochastic_oscillator","macd","bollinger","coefficient_of_variance","rsi"]
    
    def overhead(self):
        return None
    
    def signal(self,overhead,ticker_prices):
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
        ticker_prices["historical_return"] = ticker_prices["adjclose"].pct_change(5) 
        training_data = ticker_prices.iloc[:100].copy()
        for factor in self.factors:
            covariance = training_data["historical_return"].cov(training_data[factor])
            ticker_prices[f"{factor}_beta"] = covariance / ticker_prices[factor].rolling(100).var()
            ticker_prices[f"{factor}_loading"] = ticker_prices[factor] * ticker_prices[f"{factor}_beta"]
        ticker_prices[self.strategy.lower()] = [sum([row[1][f"{factor}_loading"] for factor in self.factors]) for row in ticker_prices.iterrows()]
        ticker_prices.dropna(inplace=True)
        return ticker_prices