from strategy.technical import Technical
from strategy.algo import Algo
from strategy.technical import Technical
from strategy.rolling import Rolling
from product.aproduct import AProduct
from parameter.aparameter import AParameter
import pandas as pd

tickers = pd.read_csv("tickers.csv")["ticker"].values
strategies = ["rolling","technical"]
query = {
        
        "tickers":tickers
         ,"strategies":strategies
         ,"industry_diversified":True
         ,"cfa":True
         ,"rr":0.05
         ,"risk":0.1
         ,"holding_period":5
         ,"cycle":2195
         }

aparam = AParameter()
aparam.build(query)

product = AProduct()
product.build(aparam)
product.build_strategies()
product.init_name()
product.transform()
product.model()
product.merge()
product.backtest()
product.analyze()