from parameter.aparameter import AParameter
from strategy.strategy_factory import StrategyFactory
from transformer.transformer import Transformer
from backtester.backtester import Backtester
from database.adatabase import ADatabase
import pandas as pd
from datetime import datetime
class BacktestFunctions(object):

    @classmethod
    def backtest(self,query):
        parameter = AParameter()
        parameter.build(query)
        strategy = StrategyFactory.build(parameter)
        simulation = Transformer.transform(strategy)
        results = Backtester.backtest(strategy,simulation)
        return results

    @classmethod
    def store_recommendation(self,query):
        recommendations = query["recommendations"]
        parameters = query["parameters"]
        recs = pd.DataFrame(recommendations)
        recs["date"] = datetime.now()
        for key in parameters.keys():
            recs[key] = parameters[key]
        sapling = ADatabase("sapling")
        sapling.cloud_connect()
        sapling.store("downloaded_recommendations",recs)
        sapling.disconnect()