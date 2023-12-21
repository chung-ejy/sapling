from parameter.aparameter import AParameter
from strategy.strategy_factory import StrategyFactory
from transformer.transformer import Transformer
from backtester.backtester import Backtester

class BacktestFunctions(object):

    @classmethod
    def backtest(self,query):
        parameter = AParameter()
        parameter.build(query)
        strategy = StrategyFactory.build(parameter)
        simulation = Transformer.transform(strategy)
        results = Backtester.backtest(strategy,simulation)
        return results