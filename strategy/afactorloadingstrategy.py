from strategy.anaistrategy import AStrategy
from processor.processor import Processor as processor

class AFactorLoadingStrategy(AStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)
    
    def signal(self,overhead,ticker_prices):
        ticker_prices = processor.merge(ticker_prices,overhead.copy(),on="date")
        ticker_prices["historical_return"] = ticker_prices["adjclose"].pct_change(5) 
        training_data = ticker_prices.iloc[:100].copy()
        for factor in self.factors:
            covariance = training_data["historical_return"].cov(training_data[factor])
            ticker_prices[f"{factor}_beta"] = covariance / ticker_prices[factor].rolling(100).var()
            ticker_prices[f"{factor}_loading"] = ticker_prices[factor] * ticker_prices[f"{factor}_beta"]
        ticker_prices[self.strategy.lower()] = [sum([row[1][f"{factor}_loading"] for factor in self.factors]) for row in ticker_prices.iterrows()]
        ticker_prices.dropna(inplace=True)
        return ticker_prices