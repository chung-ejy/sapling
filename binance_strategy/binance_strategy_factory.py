from binance_strategy.binance_strategy import BinanceStrategy
from binance_strategy.trailing_stoploss import TrailingStopLoss
from binance_strategy.takeprofit_market import TakeProfitMarket

class BinanceStrategyFactory(object):

    @classmethod
    def build(self,parameter):
        match parameter.strategy:
            case BinanceStrategy.TRAILING_STOPLOSS.value:
                return TrailingStopLoss(parameter)
            case BinanceStrategy.TAKEPROFIT_MARKET.value:
                return TakeProfitMarket(parameter)
            case _:
                return None
