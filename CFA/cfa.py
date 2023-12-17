from processor.processor import Processor as processor
from database.adatabase import ADatabase

fed = ADatabase("fed")
    
    
class CFA(object):
    
    @classmethod
    def cfa(self,sim,holding_period):
        fed.connect()
        benchmark = processor.column_date_processing(fed.retrieve("sp500")).rename(columns={"value":"sp500"})
        benchmark["sp500"] = [float(x) for x in benchmark["sp500"]]
        yields = processor.column_date_processing(fed.retrieve("tyields")).rename(columns={"value":"yield1"})
        yields["yield1"] = [(1+float(x)/100) ** (holding_period/365) - 1 for x in yields["yield1"]]
        sp500_projections = fed.retrieve("sp500_v2_projections").rename(columns={"prediction":"sp500_prediction"})
        fed.disconnect()

        sim = processor.merge(sim,sp500_projections,on=["year","quarter"])
        sim = processor.merge(sim,benchmark,on="date")
        sim = processor.merge(sim,yields,on="date").ffill().bfill()

        sim["sp500_var"] = sim["sp500"].rolling(100).var()
        sim["sp500_cov"] = sim["sp500"].rolling(100).cov(sim["adjclose"].rolling(50).mean())
        sim["market_expected_return"] = (sim["sp500_prediction"] - sim["sp500"]) / sim["sp500"]
        sim["market_expected_return"] = [(1+float(x)/100) ** (holding_period/365) - 1 for x in sim["market_expected_return"]]
        sim["beta"] = (sim["sp500_cov"] / sim["sp500_var"]) * float(2/3) - float(1/3)
        sim["excess_return"] = (sim["expected_return"]) - sim["yield1"] + sim["beta"] * (sim["market_expected_return"]-sim["yield1"])
        sim.sort_values("date",inplace=True)

        return sim