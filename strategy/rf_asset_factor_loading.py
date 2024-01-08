from strategy.afactorloadingstrategy import AFactorLoadingStrategy
from database.adatabase import ADatabase
from processor.processor import Processor as processor
import pandas as pd

class RFAssetFactorLoading(AFactorLoadingStrategy):

    def __init__(self,parameter):
        super().__init__(parameter)
    
    def overhead(self):
        market = ADatabase("market")
        market.cloud_connect()
        russell1000 = market.retrieve("russell1000")
        market.disconnect()
        market.cloud_connect()
        analysis = []
        for ticker in russell1000["ticker"].values:
            try:
                ticker_prices = processor.column_date_processing(market.query("prices",{"ticker":ticker}))[["date","ticker","adjclose"]]
                analysis.append({
                    "ticker":ticker,
                    "coefficient_of_variance": ticker_prices["adjclose"].std() / ticker_prices["adjclose"].mean(),
                    "return":(ticker_prices["adjclose"].iloc[-1] - ticker_prices["adjclose"].iloc[0]) / ticker_prices["adjclose"].iloc[0]
                })
            except Exception as e:
                print(str(e))
                continue
        market.disconnect()
        a = pd.DataFrame(analysis)
        a["covr"] = a["return"] / a["coefficient_of_variance"]
        self.factors = a.sort_values("covr",ascending=True).iloc[:10]["ticker"]
        
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