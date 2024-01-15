from parameter.aparameter import AParameter
from strategy.strategy_factory import StrategyFactory
from transformer.transformer import Transformer
from backtester.backtester import Backtester
from processor.server_processor import ServerProcessor
from datetime import datetime, timedelta
class BacktestFunctions(object):

    @classmethod
    def backtest(self,query):
        try:
            start = datetime.now() - timedelta(days=365.25*2)
            end = datetime.now() - timedelta(hours=24)
            parameter = AParameter()
            parameter.build(query)
            strategy = StrategyFactory.build(parameter)
            simulation = Transformer.cloud_transform(strategy,start,end)
            trades = Backtester.backtest(strategy,simulation)
            portfolio = Backtester.portfolio(trades)
            recommendations = Backtester.recommendations(trades)
            kpi = Backtester.kpi(trades,portfolio)
            results = ServerProcessor.server_format(strategy,trades,portfolio,recommendations,kpi)
        except Exception as e:
            print(str(e))
            results = {
            "portfolio":[],
            "trades":[],
            "recommendations":[],
            "kpi":{}
        }
        return results