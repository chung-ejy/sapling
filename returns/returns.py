from datetime import datetime, timedelta
class Returns(object):

    @classmethod
    def returns(self,strategy,ticker_prices):
        ticker_prices["buy_price"] = ticker_prices["adjclose"].shift(-1)
        ticker_prices["sell_price"] = ticker_prices["adjclose"].shift(-strategy.holding_period)
        ticker_prices["buy_date"] = ticker_prices["date"].shift(-1)
        ticker_prices["sell_date"] = ticker_prices["date"].shift(-strategy.holding_period)
        ticker_prices["return"] =  (ticker_prices["buy_price"] - ticker_prices["sell_price"]) / ticker_prices["sell_price"]
        ticker_prices["return"] = ticker_prices["return"] * (1/strategy.positions)
        ticker_prices["return"] = [max(float(-strategy.stop_loss/strategy.positions),x) for x in ticker_prices["return"]]
        return ticker_prices