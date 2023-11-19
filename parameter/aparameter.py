from datetime import datetime, timedelta
class AParameter(object):

    def __init__(self):
        self.cycle=100
        self.tickers=["AAPL","JPM","GS","AMZN","GOOGLE"]
        self.industry_diversified=True
        self.rolling_val=100
        self.projection_weeks=1
        self.rr=0.0
        self.risk=1
        self.skip=10
        self.today = datetime.now()
        self.extraction_date = self.today - timedelta(days=self.cycle*2) - timedelta(days=140)
        self.model_start = self.today - timedelta(days=self.cycle*2)
        self.model_end = self.today - timedelta(days=self.cycle)
        self.backtest_start = self.model_end
        self.backtest_end = self.today

    def build(self,query):
        for key in query.keys():
            self.__setattr__(key,query[key])
        self.today = datetime.now()
        self.extraction_date = self.today - timedelta(days=self.cycle*2) - timedelta(days=140)
        self.model_start = self.today - timedelta(days=self.cycle*2)
        self.model_end = self.today - timedelta(days=self.cycle)
        self.backtest_start = self.model_end
        self.backtest_end = self.today
            