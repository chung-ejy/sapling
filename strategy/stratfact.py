from strategy.strategy import Strategy
from strategy.algo import Algo
from strategy.rolling import Rolling
from strategy.technical import Technical
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
            case _:
                return ""