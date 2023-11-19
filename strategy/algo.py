from strategy.astrategy import AStrategy
import pandas as pd
class Algo(AStrategy):

    def __init__(self,cycle,tickers,rolling_val,projection_weeks,rr,risk,skip):
        super().__init__("algo",cycle,tickers,rolling_val,projection_weeks,rr,risk,skip)
        self.projection_horizon = 5
    
    def model(self):
        return pd.DataFrame([{"model":"nonai"}])
    
    def sim(self):
        sim = []
        self.market.connect()
        for ticker in self.tickers[::self.skip]:
            try:
                prices = self.processor.column_date_processing(self.market.query("prices",{"ticker":ticker}))
                prices["prediction"] = prices["adjclose"].rolling(self.rolling_val).mean()
                sim.append(prices.iloc[self.rolling_val:].fillna(1))
            except Exception as e:
                continue
        self.market.disconnect()
        simulation = pd.concat(sim)
        return simulation
    
    def backtest(self,simulation):
        trades = simulation[simulation["weekday"]==4]
        trades = trades[(trades["week"] % self.projection_weeks) + 1 == 1]
        trades = trades[trades["risk"]<=self.risk]
        trades = trades[trades["abs"]>=self.rr]
        trades = trades.sort_values("abs",ascending=False).groupby(["date"]).first().reset_index()
        trades["cr"] = trades["return"].cumprod() * 100
        trades.sort_values("date",inplace=True)
        return trades

    def signals(self,prices):
        prices["std"] = prices["adjclose"].rolling(self.rolling_val).std()
        prices["risk"] = prices["std"] / prices["prediction"]
        prices["signal"] = (prices["prediction"] - prices["adjclose"]) / prices["adjclose"]
        prices["abs"] = prices["signal"].abs()
        prices["direction"] = prices["signal"] / prices["abs"]
        return prices
    
    def returns(self,prices):    
        prices["buy_price"] = prices["adjclose"].shift(-1)
        prices["buy_date"] = prices["date"].shift(-1)
        prices["sell_price"] = prices["adjclose"].shift(-self.projection_days)
        prices["sell_date"] = prices["date"].shift(-self.projection_days)
        prices["return"] = (prices["sell_price"] - prices["buy_price"]) / prices["buy_price"] * prices["direction"] + 1
        return prices