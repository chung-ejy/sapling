from product.aproduct import AProduct
from parameter.aparameter import AParameter
from database.adatabase import ADatabase

market = ADatabase("market")
market.connect()
sp100 = market.retrieve("sp100")
market.disconnect()
strategies = [
                "metrics",
              "technical",
              "rolling",
              "algo"
              ]

query = {
        
        "tickers":sp100["ticker"].values
         ,"strategies":strategies
         ,"industry_diversified":False
         ,"cfa":False
         ,"rr":0.00
         ,"risk":1
         ,"holding_period":5
         ,"cycle":1800
         
         }

aparam = AParameter()
aparam.build(query)

product = AProduct(True)
product.build(aparam)
product.build_strategies()
product.init_name()
product.transform_strats()
product.model_strats()
product.transform()
product.model()
product.backtest()
product.analyze()