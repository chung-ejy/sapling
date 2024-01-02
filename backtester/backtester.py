from datetime import datetime
import warnings
warnings.simplefilter(action="ignore")
class Backtester(object):

    @classmethod
    def backtest(self,strategy,simulation):
        today = datetime.now()
        weekday = today.weekday() - 1 if today.weekday() != 0 and today.weekday() < 4 else 4
        week = today.isocalendar()[1] if today.weekday() != 0 and today.weekday() < 4 else today.isocalendar()[1] - 1
        week_mod = int(week % (strategy.holding_period/5))

        trades = simulation[simulation["weekday"]==weekday].copy()
        trades = trades[trades["week"] % int(strategy.holding_period/5) == week_mod]
        
        iteration_trades = trades.copy().sort_values("signal",ascending=False).groupby(["date"]).nth([i for i in range(strategy.positions)]).reset_index()
        iteration_trades.sort_values("date",inplace=True)
        recommendations = iteration_trades[iteration_trades["date"]==iteration_trades["date"].max()]
        
        portfolio = iteration_trades[["date","return"]].groupby("date").sum().reset_index()
        portfolio.sort_values("date",inplace=True)
        portfolio["year"] = [x.year for x in portfolio["date"]]
        portfolio["return"] = portfolio["return"] + 1
        portfolio["cumulative_return"] = portfolio["return"].cumprod()
        
        trades["date"] = [str(x).split(" ")[0] for x in trades["date"]]
        recommendations["date"] = [str(x).split(" ")[0] for x in recommendations["date"]]

        return {
            "portfolio":portfolio.round(4).to_dict("records"),
            "trades":trades.round(4).to_dict("records"),
            "recommendations":recommendations.round(4).to_dict("records")
        }