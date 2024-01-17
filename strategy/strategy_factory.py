from strategy.strategy import Strategy
from strategy.coefficient_of_variance import CoefficientOfVariance
from strategy.average_return import AverageReturn
from strategy.standard_deviation import StandardDeviation
from strategy.skew import Skew
from strategy.kurtosis import Kurtosis
from strategy.moving_average import MovingAverage
from strategy.bollinger import Bollinger
from strategy.bollinger_width import BollingerWidth
from strategy.rsi import RSI
from strategy.macd import MACD
from strategy.stochastic_oscillator import StochasticOscillator
from strategy.random import Random
from strategy.tech_factor_loading import TechFactorLoading
from strategy.tech_ai import TechAI
from strategy.technical import Technical
from strategy.rf_asset_factor_loading import RFAssetFactorLoading
from strategy.rsi_to_coev import RSIToCoev

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
            case Strategy.BOLLINGER.value:
                return Bollinger(parameter)
            case Strategy.BOLLINGER_WIDTH.value:
                return BollingerWidth(parameter)
            case Strategy.RSI.value:
                return RSI(parameter)
            case Strategy.MACD.value:
                return MACD(parameter)
            case Strategy.STOCHASTIC_OSCILLATOR.value:
                return StochasticOscillator(parameter)
            case Strategy.RANDOM.value:
                return Random(parameter)
            case Strategy.TECH_FACTOR_LOADING.value:
                return TechFactorLoading(parameter)
            case Strategy.TECH_AI.value:
                return TechAI(parameter)
            case Strategy.TECHNICAL.value:
                return Technical(parameter)
            case Strategy.RSI_TO_COEV.value:
                return RSIToCoev(parameter)
            case _:
                return None
