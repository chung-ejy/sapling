import pandas as pd
from database.adatabase import ADatabase

class AMetric(object):

    def __init__(self,name :str):
        self.name = name
        self.ascending = True
        self.db = ADatabase(self.name)
        self.ascending = True
        self.positions = 1
        self.holding_period = 7
        
    def supplementary(self):
        self.db.connect()
        supplementary = self.db.retrieve("supplementary")
        self.db.disconnect()
        return supplementary
    
    def create_metric(self,price:pd.DataFrame):
        price["metric"] = price["adjclose"]
        return price
    
    def buy_clause(self,position: pd.DataFrame, recommendation:pd.DataFrame):
        return True
    
    def sell_clause(self,position: pd.DataFrame, recommendation:pd.DataFrame):
        # return (recommendation["date"] - position["buy_date"]).days > self.holding_period
        return recommendation["ticker"] != position["symbol"]
    
    def preprocessing(self,sim: pd.DataFrame,prices:pd.DataFrame):
        final = prices.merge(sim[["ticker",self.name]],on=["ticker"],how="left").dropna()
        return final
    
    def position_merge(self,positions:pd.DataFrame,recommendations:pd.DataFrame):
        return positions.rename(columns={"symbol":"ticker"}).merge(recommendations [["ticker",self.name]],on="ticker",how="left") 
    
    def buy_position_filter(self,i: int,recommendations:pd.DataFrame,orders:pd.DataFrame,positions:pd.DataFrame):
        recommendation = recommendations.iloc[i]
        recommendation_order = pd.DataFrame([]) if orders.index.size < 1 else orders[orders["symbol"]==recommendation["ticker"]] 
        position = pd.DataFrame([]) if positions.index.size < 1 else positions[positions["symbol"]==recommendation["ticker"]]
        return recommendation, recommendation_order, position

    def sell_position_filter(self,i: int,recommendations:pd.DataFrame,orders:pd.DataFrame,positions:pd.DataFrame):
        recommendation = recommendations.iloc[i]
        recommendation_order = pd.DataFrame([]) if orders.index.size < 1 else orders[orders["symbol"]==recommendation["ticker"]] 
        position = positions.iloc[i]
        return recommendation, recommendation_order, position