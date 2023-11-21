from product.aproduct import AProduct
from parameter.aparameter import AParameter
from database.adatabase import ADatabase

market = ADatabase("market")
market.connect()
sp100 = market.retrieve("sp100")
market.disconnect()
strategies = [
              "algo"
              ]

query = {
        
        "tickers":sp100["ticker"].values
         ,"strategies":strategies
         ,"industry_diversified":True
         ,"cfa":True
         ,"rr":0.00
         ,"risk":1
         ,"holding_period":5
         ,"cycle":365
         
         }

aparam = AParameter()
aparam.build(query)

product = AProduct(False)
product.build(aparam)
product.build_strategies()
product.init_name()
product.transform_strats()
product.model_strats()
product.transform()
product.model()
product.backtest()
product.analyze()