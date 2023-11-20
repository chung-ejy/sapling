import pandas as pd

class Transformer(object):

    @classmethod
    def checkpoint(self,strategy):
        strategy.market.connect()
        strategy.drop_model_data()
        for ticker in strategy.parameter.tickers:
            try:
                ticker_data = strategy.transform(ticker)
                strategy.store_model_data(ticker_data)
            except Exception as e:
                print(ticker,print(str(e)))
        strategy.market.disconnect()
        
        