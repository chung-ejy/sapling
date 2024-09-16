from metric.metric import Metric
from metric.average_return import AverageReturn
from metric.previous_return import PreviousReturn
from metric.coefficient_of_variance import CoefficientOfVariance
from metric.return_to_risk import ReturnToRisk
from metric.bollinger import Bollinger
from metric.rsi import RSI
class MetricFactory(object):

    @classmethod
    def build(self,metric: Metric):
        match metric:
            case Metric.AVERAGE_RETURN:
                return AverageReturn()
            case Metric.PREVIOUS_RETURN:
                return PreviousReturn()
            case Metric.COEFFICIENT_OF_VARIANCE:
                return CoefficientOfVariance()
            case Metric.RETURN_TO_RISK:
                return ReturnToRisk()
            case Metric.BOLLINGER:
                return Bollinger()
            case Metric.RSI:
                return RSI()
            case _:
                return None