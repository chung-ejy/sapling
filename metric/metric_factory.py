from metric.metric import Metric
from metric.average_return import AverageReturn
from metric.previous_return import PreviousReturn
from metric.coefficient_of_variance import CoefficientOfVariance
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
            case _:
                return None