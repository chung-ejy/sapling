from processor.processor import Processor as processor
import pandas as pd
from database.adatabase import ADatabase
from datetime import datetime
class Backtester(object):

    @classmethod
    def backtest(self,strategy,simulation):
        simulation["return"] = simulation["return"] * (1/strategy.positions) *0.99
        simulation["return"] = [max(float(-strategy.stop_loss/strategy.positions),x) for x in simulation["return"]]
        today = datetime.now()
        weekday = today.weekday() - 1 if today.weekday() != 0 else 4
        week = today.isocalendar()[1] if today.weekday() != 0 else today.isocalendar()[1] - 1
        week_mod = int(week % (strategy.holding_period/5))
        fed = ADatabase("fed")
        fed.connect()
        bench = fed.retrieve("sp500")
        bench["date"] = pd.to_datetime(bench["date"],utc=True)
        bench["value"] = [float(x) for x in bench["value"]]
        fed.disconnect()
        trades = simulation[simulation["weekday"]==weekday].copy()
        trades = trades[trades["week"] % int(strategy.holding_period/5) == week_mod]
        trades = processor.column_date_processing(trades)
        iteration_trades = trades.copy().sort_values("signal",ascending=False).groupby(["date"]).nth([i for i in range(strategy.positions)]).reset_index()
        portfolio = iteration_trades[["date","return"]].groupby("date").sum().reset_index()
        portfolio.sort_values("date",inplace=True)
        portfolio["year"] = [x.year for x in portfolio["date"]]
        portfolio["return"] = portfolio["return"] + 1
        portfolio["cumulative_return"] = portfolio["return"].cumprod()
        portfolio = processor.column_date_processing(portfolio)
        portfolio = processor.merge(portfolio,bench.copy(),on="date")
        portfolio.dropna(inplace=True)
        portfolio["bench_cum_return"] = (portfolio["value"] - portfolio["value"].iloc[0]) / portfolio["value"].iloc[0] + 1
        portfolio["beta"] = portfolio["cumulative_return"].cov(portfolio["value"])
        portfolio["treynor"] = portfolio["cumulative_return"] / portfolio["beta"]
        portfolio["excess_return"] = portfolio["cumulative_return"] - portfolio["bench_cum_return"]
        return {
            "portfolio":portfolio.to_dict("records"),
            "trades":iteration_trades.to_dict("records")
        }