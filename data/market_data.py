from asset.exposure import Exposure
from datetime import datetime
class MarketData(object):

    def __init__(self,date=datetime.now(),ticker="",adjclose=0.0,factor=0.0,exposure=Exposure.LONG,rf=0.0):
        self.date = date
        self.ticker = ticker
        self.adjclose = adjclose
        self.factor = factor
        self.exposure = exposure
        self.rf = rf
    
    @staticmethod
    def build(row):
        result = MarketData()
        result.date = row["date"]
        result.ticker = row["ticker"]
        result.adjclose = row["adjclose"]
        result.factor = row["factor"]
        result.exposure = row["exposure"]
        result.rf = row["rf"]
        return result