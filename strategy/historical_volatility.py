from datetime import timedelta

class HistoricalVolatility(object):

    def __init__(self,parameter):
        for key in parameter.__dict__.keys():
            self.__setattr__(key,parameter.__dict__[key])

    def signal(self,ticker_prices):
        ticker_prices.sort_values("date",inplace=True)
        simulation = ticker_prices.copy()
        simulation.sort_values("date",inplace=True)
        simulation["signal"] = simulation["adjclose"].rolling(100).std() / simulation["adjclose"].rolling(100).mean()
        simulation["buy_price"] = simulation["adjclose"]
        simulation["buy_date"] = simulation["date"].shift(-1)
        simulation["sell_price"] = simulation["adjclose"].shift(-self.holding_period)
        simulation["sell_date"] = simulation["date"] + timedelta(days=int(self.holding_period /5) * 7)
        simulation["return"] = (simulation["sell_price"] - simulation["buy_price"]) / simulation ["buy_price"]
        return simulation