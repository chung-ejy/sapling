class ServerProcessor(object):

    @classmethod
    def server_format(self,strategy,trades,portfolio,recommendations,kpi):
        trade_columns = ["date","buy_date","sell_date","ticker","adjclose",strategy.strategy.lower(),"buy_price","sell_price","return"]
        recs_columns = ["date","buy_date","sell_date","ticker","adjclose",strategy.strategy.lower()]

        for column in ["date","sell_date","buy_date"]:
            trades[column] = [str(x).split(" ")[0] for x in trades[column]]
            recommendations[column] = [str(x).split(" ")[0] for x in recommendations[column]]
        
        trades = trades[trade_columns].dropna().round(4).to_dict("records")
        recommendations = recommendations[recs_columns].dropna().round(4).to_dict("records")
        portfolio = portfolio.round(4).to_dict("records")
        
        return {
            "portfolio":portfolio,
            "trades":trades,
            "recommendations":recommendations,
            "kpi":kpi
        }