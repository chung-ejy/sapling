from strategy.astrategy import AStrategy
import pandas as pd
from parameters.aparameters import AParameters

class AverageReturnStrategy(AStrategy):

    def __init__(self,parameters: AParameters):
        super().__init__("average_return",parameters)
        self.ranker = "average_return"
        self.ascending = True

    def buy_clause(self,position: pd.DataFrame, recommendation:pd.DataFrame):
        return True
    
    def sell_clause(self,position: pd.DataFrame, recommendation:pd.DataFrame):
        return position["ticker"] != recommendation["ticker"]
    
    def preprocessing(self,sim: pd.DataFrame,prices:pd.DataFrame):
        sim = prices.merge(sim[["date","ticker","average_return"]],on=["date","ticker"],how="left").dropna()
        return sim
    
    def position_merge(self,positions:pd.DataFrame,recommendations:pd.DataFrame):
        return positions.rename(columns={"symbol":"ticker"}).merge(recommendations [["ticker",self.strategy.ranker]],on="ticker",how="left") 
    
    def buy_position_filter(self,i: int,recommendations:pd.DataFrame,orders:pd.DataFrame,positions:pd.DataFrame):
        recommendation = recommendations.iloc[i]
        recommendation_order = pd.DataFrame([]) if orders.index.size < 1 else orders[orders["symbol"]==recommendation["ticker"]] 
        position = positions.iloc[i]
        return recommendation, recommendation_order, position

    def sell_position_filter(self,i: int,recommendations:pd.DataFrame,orders:pd.DataFrame,positions:pd.DataFrame):
        recommendation = recommendations.iloc[i]
        recommendation_order = pd.DataFrame([]) if orders.index.size < 1 else orders[orders["symbol"]==recommendation["ticker"]] 
        position = positions.iloc[i]
        return recommendation, recommendation_order, position