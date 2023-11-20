from product.aproduct import AProduct
from parameter.aparameter import AParameter
from database.adatabase import ADatabase

market = ADatabase("market")
market.connect()
sp100 = market.retrieve("sp100")
market.disconnect()
strategies = ["rolling","technical"]

query = {
        
        "tickers":sp100["ticker"].values
         ,"strategies":strategies
         ,"industry_diversified":True
         ,"cfa":True
         ,"rr":0.05
         ,"risk":0.1
         ,"holding_period":5
         ,"cycle":365
         
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