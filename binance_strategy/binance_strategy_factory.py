from binance_strategy.binance_strategy import BinanceStrategy
from binance_strategy.trailing_stoploss import TrailingStopLoss

class BinanceStrategyFactory(object):

    @classmethod
    def build(self,parameter):
        match parameter.strategy:
            case BinanceStrategy.TRAILING_STOPLOSS.value:
                return TrailingStopLoss(parameter)
            case _:
                return None
