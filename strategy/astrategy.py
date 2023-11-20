from book.abook import ABook
from datetime import datetime, timedelta
from parameter.aparameter import AParameter

class AStrategy(ABook):

    def __init__(self,name):
        super().__init__(name)

    def build(self,parameter):
        self.parameter = parameter
        self.today = datetime.now()
        self.extraction_date = self.today - timedelta(days=self.parameter.cycle*2) - timedelta(days=140)
        self.model_start = self.today - timedelta(days=self.parameter.cycle*2)
        self.model_end = self.today - timedelta(days=self.parameter.cycle)
        self.backtest_start = self.model_end
        self.backtest_end = self.today
    
    def transform(self,ticker):
        prices = self.market.query("prices",{"ticker":ticker})
        prices = self.processor.column_date_processing(prices)
        return prices[["year","quarter","month","week","weekday","date","ticker","adjclose"]]