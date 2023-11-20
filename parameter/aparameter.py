class AParameter(object):

    def __init__(self):
        self.tickers=["AAPL","JPM","GS","AMZN","GOOG","TSLA","MO",
                      "PYPAL","MA","INTC","NVDA","F","MO","JNJ"]
        self.cycle=1460
        self.holding_period = 5
        self.industry_diversified=True
        self.rr=0.05
        self.risk=0.1
        self.cfa = False
        self.strategies = ["algo"]
        
    def build(self,query):
        for key in query.keys():
            self.__setattr__(key,query[key])