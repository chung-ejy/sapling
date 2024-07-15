from strategy.astrategy import AStrategy
import pandas as pd
from parameter.aparameter import AParameter

class FundamentalStrategy(AStrategy):

    def __init__(self,parameters: AParameter):
        super().__init__("fundamental",parameters)
        self.ranker = "expected_return"
        self.ascending = False

    def buy_clause(self,position: pd.DataFrame, recommendation:pd.DataFrame):
        return True
    
    def sell_clause(self,position: pd.DataFrame, recommendation:pd.DataFrame):
        return position["ticker"] != recommendation["ticker"] and position["expected_return"] <= 0
    
    def preprocessing(self,sim: pd.DataFrame,prices:pd.DataFrame):
        sim = prices.merge(sim[["ticker","GICS Sector","prediction"]],on=["ticker"],how="left").dropna()
        sim["expected_return"] = (sim["prediction"] - sim["adjclose"]) / sim["adjclose"]
        return sim
    
    def position_merge(self,positions:pd.DataFrame,recommendations:pd.DataFrame):
        return positions.rename(columns={"symbol":"ticker"}).merge(recommendations [["ticker","GICS Sector",self.ranker]],on="ticker",how="left")

    def buy_position_filter(self,i: int,recommendations:pd.DataFrame,orders:pd.DataFrame,positions:pd.DataFrame):
        sectors = list(recommendations["GICS Sector"].unique())
        sectors.sort()
        sector = sectors[i] 
        recommendation = recommendations[recommendations["GICS Sector"]==sector].iloc[0]
        recommendation_order = pd.DataFrame([]) if orders.index.size < 1 else orders[orders["symbol"]==recommendation["ticker"]] 
        position =  pd.DataFrame([]) if positions.index.size < 1 else positions[positions["symbol"]==recommendation["ticker"]] 
        return recommendation, recommendation_order, position

    def sell_position_filter(self,i: int,recommendations:pd.DataFrame,orders:pd.DataFrame,positions:pd.DataFrame):
        sectors = list(recommendations["GICS Sector"].unique())
        sectors.sort()
        sector = sectors[i] 
        recommendation = recommendations[recommendations["GICS Sector"]==sector].iloc[0]
        recommendation_order = pd.DataFrame([]) if orders.index.size < 1 else orders[orders["symbol"]==recommendation["ticker"]] 
        position = positions[positions["GICS Sector"]==sector]
        return recommendation, recommendation_order, position
    