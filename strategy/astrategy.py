from parameter.aparameter import AParameter
import pandas as pd
class AStrategy(object):

    def __init__(self,name :str, parameters: AParameter):
        self.name = name
        self.parameters = parameters
        self.ranker = "price"
        self.ascending = "True"

    def buy_clause(self,position: pd.DataFrame, recommendation:pd.DataFrame):
        return True
    
    def sell_clause(self,position: pd.DataFrame, recommendation:pd.DataFrame):
        return True
    
    def preprocessing(self,sim: pd.DataFrame,prices:pd.DataFrame):
        return pd.DataFrame()
    
    def position_merge(self,positions:pd.DataFrame,recommendations:pd.DataFrame):
        return pd.Dataframe()
    
    def buy_position_filter(self,i: int,recommendations:pd.DataFrame,orders:pd.DataFrame,positions:pd.DataFrame):
        return [pd.Dataframe(), pd.Dataframe(), pd.Dataframe()]
    
    def sell_position_filter(self,i: int,recommendations:pd.DataFrame,orders:pd.DataFrame,positions:pd.DataFrame):
        return [pd.Dataframe(), pd.Dataframe(), pd.Dataframe()]