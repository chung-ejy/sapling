
class AParameter(object):

    def __init__(self):
        self.positions = 10
        self.strategy = "HISTORICAL_VOLATILITY"
        self.holding_period = 5
        self.stop_loss = 0.05
    
    def build(self,query):
        for key in query.keys():
            self.__setattr__(key,query[key])
            