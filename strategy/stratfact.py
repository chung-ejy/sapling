from strategy.strategy import Strategy
from strategy.algo import Algo
from strategy.rolling import Rolling
from strategy.technical import Technical
from strategy.bollinger import Bollinger
class StratFact(object):

    @classmethod
    def factory(self,strat_string):

        match strat_string:
            case Strategy.TECHNICAL.value:
                return Technical()
            case Strategy.ROLLING.value:
                return Rolling()
            case Strategy.ALGO.value:
                return Algo()
            case Strategy.BOLLINGER.value:
                return Bollinger()
            case _:
                return ""