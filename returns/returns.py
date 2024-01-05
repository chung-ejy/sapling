from datetime import datetime, timedelta
class Returns(object):

    @classmethod
    def returns(self,strategy,ticker_prices):
        sell_day_shift = int(strategy.holding_period / 5 * 7)
        ticker_prices["buy_price"] = ticker_prices["adjclose"].shift(-1)
        ticker_prices["sell_price"] = ticker_prices["adjclose"].shift(-5)
        ticker_prices["buy_date"] = [x + timedelta(days=1) if x.weekday() < 4 else x + timedelta(days=7-x.weekday()) for x in ticker_prices["date"]]
        ticker_prices["sell_date"] = ticker_prices["date"] + timedelta(days=sell_day_shift)
        ticker_prices["return"] =  (ticker_prices["sell_price"] - ticker_prices["buy_price"]) / ticker_prices["buy_price"]
        ticker_prices["return"] = ticker_prices["return"] * (1/strategy.positions)
        ticker_prices["return"] = [max(float(-strategy.stop_loss/strategy.positions),x) for x in ticker_prices["return"]]
        return ticker_prices