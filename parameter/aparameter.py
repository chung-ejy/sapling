
class AParameter(object):

    def __init__(self):
        self.positions = 10
        self.strategy = "HISTORICAL_VOLATILITY"
        self.holding_period = 5
        self.stop_loss = 0.05
    
    def build(self,query):
        for key in query.keys():
            match key:
                case "holding_period":
                    self.__setattr__(key,int(query[key]))
                case "positions":
                    self.__setattr__(key,int(query[key]))
                case "stop_loss":
                    self.__setattr__(key,float(query[key]))
                case "strategy":
                    self.__setattr__(key,query[key])
            