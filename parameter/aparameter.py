
class AParameter(object):

    def __init__(self):
        self.positions = 5
        self.strategy = "RSI"
        self.holding_period = 5
        self.stop_loss = 0.05
        self.ascending = False
        self.tickers = ["AMZN"]
        
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
                    self.__setattr__(key,str(query[key]))
                case "ascending":
                    self.__setattr__(key,bool(query[key]))
                case "tickers":
                    self.__setattr__(key,list(query[key]))

            