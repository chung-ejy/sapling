from strategy.afactorloadingstrategy import AFactorLoadingStrategy

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
            training_data[f"{factor}_beta"] = covariance / training_data[factor].rolling(100).var()
            training_data[f"{factor}_loading"] = training_data[factor] * training_data[f"{factor}_beta"]
        training_data[self.strategy.lower()] = [sum([row[1][f"{factor}_loading"] for factor in self.factors]) for row in training_data.iterrows()]
        training_data.dropna(inplace=True)
        return training_data