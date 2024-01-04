from datetime import datetime, timedelta
import warnings
warnings.simplefilter(action="ignore")
import pandas as pd

class Backtester(object):

    @classmethod
    def backtest(self,strategy,simulation):
        today = datetime.now()
        weekday = today.weekday() - 1 if today.weekday() != 0 and today.weekday() < 4 else 4
        # week = today.isocalendar()[1] if today.weekday() != 0 and today.weekday() < 4 else today.isocalendar()[1] - 1
        # week_mod = int(week % (strategy.holding_period/5))

        trades = simulation[simulation["weekday"]==weekday].copy()
        # trades = trades[trades["week"] % int(strategy.holding_period/5) == week_mod]
        trades.sort_values("date",inplace=True)

        iteration_trades = trades.copy().sort_values("signal",ascending=strategy.ascending).groupby(["date"]).nth([i for i in range(strategy.positions)]).reset_index()
        iteration_trades.sort_values("date",inplace=True)
        
        recommendations = iteration_trades[iteration_trades["date"]==iteration_trades["date"].max()].copy().drop(["sell_price","buy_price","return"],axis=1)
        
        portfolio = iteration_trades[["date","return"]].groupby("date").sum().reset_index()
        portfolio.sort_values("date",inplace=True)
        portfolio = portfolio.iloc[:-1]
        portfolio["year"] = [x.year for x in portfolio["date"]]
        portfolio["return"] = portfolio["return"] + 1
        portfolio["cumulative_return"] = portfolio["return"].cumprod()

        for column in ["date","sell_date","buy_date"]:
            iteration_trades[column] = [str(x).split(" ")[0] for x in iteration_trades[column]]
            recommendations[column] = [str(x).split(" ")[0] for x in recommendations[column]]

        results = {}
        results["number_of_trades"] = iteration_trades.index.size
        results["std"] = portfolio["cumulative_return"].std()
        results["coefficient_of_variance"] = portfolio["cumulative_return"].std() / portfolio["cumulative_return"].mean()
        results["sharpe"] = portfolio["cumulative_return"].iloc[-1] / portfolio["cumulative_return"].std()
        results["return"] = portfolio["cumulative_return"].iloc[-1]
        results = pd.DataFrame([results]).round(4).to_dict("records")[0]

        return {
            "portfolio":portfolio.dropna().round(4).to_dict("records"),
            "trades":iteration_trades[iteration_trades["date"]<iteration_trades["date"].max()].dropna().round(4).to_dict("records"),
            "recommendations":recommendations.dropna().round(4).to_dict("records"),
            "kpi":results
        }