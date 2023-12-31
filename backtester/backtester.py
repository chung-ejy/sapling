from datetime import datetime
from database.adatabase import ADatabase
import warnings
warnings.simplefilter(action="ignore")
import pandas as pd

class Backtester(object):

    @classmethod
    def backtest(self,strategy,simulation):
        today = datetime.now()
        weekday = today.weekday() - 1 if today.weekday() != 0 and today.weekday() < 4 else 4
        trades = simulation[simulation["weekday"]==weekday].copy()
        trades.sort_values("date",inplace=True)
        iteration_trades = trades.copy().sort_values(strategy.strategy.lower(),ascending=strategy.ascending).groupby(["date"]).nth([i for i in range(strategy.positions)]).reset_index()
        iteration_trades.sort_values("date",inplace=True)
        return iteration_trades
    
    @classmethod
    def portfolio(self,iteration_trades):
        portfolio = iteration_trades[["date","return"]].groupby("date").sum().reset_index()
        portfolio.sort_values("date",inplace=True)
        portfolio = portfolio.iloc[:-1]
        portfolio["year"] = [x.year for x in portfolio["date"]]
        portfolio["return"] = portfolio["return"] + 1
        portfolio["cumulative_return"] = (portfolio["return"].cumprod() - 1) * 100
        return portfolio
    
    @classmethod
    def recommendations(self,iteration_trades):    
        recommendations = iteration_trades[iteration_trades["date"]==iteration_trades["date"].max()].copy()
        return recommendations
    
    @classmethod
    def kpi(self,iteration_trades,portfolio):
        results = {}
        results["number_of_trades"] = iteration_trades.index.size
        results["standard_deviation"] = portfolio["cumulative_return"].std()
        results["coefficient_of_variance"] = portfolio["cumulative_return"].std() / portfolio["cumulative_return"].mean()
        results["sharpe"] = portfolio["cumulative_return"].iloc[-1] / portfolio["cumulative_return"].std()
        results["return"] = portfolio["cumulative_return"].iloc[-1]
        results = pd.DataFrame([results]).round(4).to_dict("records")[0]
        return results

    @classmethod
    def market(self):
        db = ADatabase("sapling")
        db.cloud_connect()
        results = db.retrieve("kpi").drop("standard_deviation",axis=1).dropna()
        db.disconnect()
        return results