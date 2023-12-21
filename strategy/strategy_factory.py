from strategy.strategy import Strategy
from strategy.historical_volatility import HistoricalVolatility
class StrategyFactory(object):

    @classmethod
    def build(self,parameter):
        match parameter.strategy:
            case Strategy.HISTORICAL_VOLATILIY.value:
                return HistoricalVolatility(parameter)
            case _:
                return None
