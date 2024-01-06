class ServerProcessor(object):

    @classmethod
    def server_format(self,strategy,trades,portfolio,recommendations,kpi):
        included_columns = ["date","buy_date","sell_date","week","weekday","ticker","adjclose",strategy.strategy.lower(),"buy_price","sell_price","return"]
        trades = trades[included_columns]
        for column in ["date","sell_date","buy_date"]:
            trades[column] = [str(x).split(" ")[0] for x in trades[column]]
            recommendations[column] = [str(x).split(" ")[0] for x in recommendations[column]]
        
        return {
            "portfolio":portfolio.round(4).to_dict("records"),
            "trades":trades[trades["date"]<trades["date"].max()].round(4).to_dict("records"),
            "recommendations":recommendations.round(4).to_dict("records"),
            "kpi":kpi
        }