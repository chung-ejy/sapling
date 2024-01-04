from strategy.afactorloadingstrategy import AFactorLoadingStrategy
from database.adatabase import ADatabase
from processor.processor import Processor as processor
import pandas as pd

class TechFactorLoading(AFactorLoadingStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)
        self.factors = ["AMZN","GOOGL","AAPL"]
    
    def overhead(self):
        market = ADatabase("market")
        market.cloud_connect()
        factor_dfs = []
        for ticker in self.factors:
            try:
                ticker_prices = processor.column_date_processing(market.query("prices",{"ticker":ticker}))[["date","ticker","adjclose"]]
                ticker_prices["historical_return"] = ticker_prices["adjclose"].pct_change(5) 
                factor_dfs.append(ticker_prices)
            except Exception as e:
                print(str(e))
                continue
        market.disconnect()
        factor_df = pd.concat(factor_dfs).pivot_table(index="date",columns="ticker",values="historical_return").reset_index()
        return factor_df