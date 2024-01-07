from parameter.aparameter import AParameter
from strategy.strategy_factory import StrategyFactory
from transformer.transformer import Transformer
from backtester.backtester import Backtester
from processor.server_processor import ServerProcessor

class BacktestFunctions(object):

    @classmethod
    def backtest(self,query):
        parameter = AParameter()
        parameter.build(query)
        strategy = StrategyFactory.build(parameter)
        simulation = Transformer.transform(strategy)
        trades = Backtester.backtest(strategy,simulation)
        portfolio = Backtester.portfolio(trades)
        recommendations = Backtester.recommendations(trades)
        kpi = Backtester.kpi(trades,portfolio)
        results = ServerProcessor.server_format(strategy,trades,portfolio,recommendations,kpi)
        return results
