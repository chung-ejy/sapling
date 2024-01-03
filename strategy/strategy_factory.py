from strategy.strategy import Strategy
from strategy.coefficient_of_variance import CoefficientOfVariance
from strategy.average_return import AverageReturn
from strategy.standard_deviation import StandardDeviation
from strategy.skew import Skew
from strategy.kurtosis import Kurtosis
from strategy.moving_average import MovingAverage
class StrategyFactory(object):

    @classmethod
    def build(self,parameter):
        match parameter.strategy:
            case Strategy.COEFFICIENT_OF_VARIANCE.value:
                return CoefficientOfVariance(parameter)
            case Strategy.AVERAGE_RETURN.value:
                return AverageReturn(parameter)
            case Strategy.STANDARD_DEVIATION.value:
                return StandardDeviation(parameter)
            case Strategy.SKEW.value:
                return Skew(parameter)
            case Strategy.KURTOSIS.value:
                return Kurtosis(parameter)
            case Strategy.MOVING_AVERAGE.value:
                return MovingAverage(parameter)
            case _:
                return None
