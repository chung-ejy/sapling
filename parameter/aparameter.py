
class AParameter(object):

    def __init__(self):
        
        self.strategy = "AVERAGE_RETURN"
        self.diversifier = "SIMPLE"
        self.holding_period = 5
        self.stop_loss = 1
        self.ascending = True
        self.tickers = ["AMZN"]
        self.prices = "prices"

    def build(self,query):
        for key in query.keys():
            match key:
                case "holding_period":
                    self.__setattr__(key,int(query[key]))
                case "stop_loss":
                    self.__setattr__(key,float(query[key]))
                case "strategy":
                    self.__setattr__(key,str(query[key]))
                case "diversifier":
                    self.__setattr__(key,str(query[key]))
                case "ascending":
                    self.__setattr__(key,bool(query[key]))
                case "tickers":
                    self.__setattr__(key,list(query[key]))
                case "prices":
                    self.__setattr__(key,str(query[key]))

            