from strategy.strategy import Strategy
from parameter.aparameter import AParameter
from strategy.average_return import AverageReturn
from strategy.previous_return import PreviousReturn
class StrategyFactory(object):

    @classmethod
    def build(self,strategy: Strategy,parameters:AParameter):
        match strategy:
            case Strategy.AVERAGE_RETURN:
                return AverageReturn(parameters=parameters)
            case Strategy.PREVIOUS_RETURN:
                return PreviousReturn(parameters=parameters)
            case _:
                return None