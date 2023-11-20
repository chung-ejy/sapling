import pandas as pd
from tqdm import tqdm
class Transformer(object):

    @classmethod
    def checkpoint(self,strategy):
        strategy.market.connect()
        strategy.drop_model_data()
        for ticker in tqdm(strategy.parameter.tickers,desc="transformation"):
            try:
                ticker_data = strategy.transform(ticker)
                strategy.store_model_data(ticker_data)
            except Exception as e:
                print(ticker,print(str(e)))
        strategy.market.disconnect()
        
        