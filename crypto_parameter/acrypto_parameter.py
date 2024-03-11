
class ACryptoParameter(object):

    def __init__(self):
        self.strategy = "TRAILING_STOPLOSS"

    def build(self,query):
        for key in query.keys():      
            match key:
                case "band":
                    self.__setattr__(key,int(query[key]))
                case "profittake":
                    self.__setattr__(key,float(query[key]))
                case "stoploss":
                    self.__setattr__(key,float(query[key]))
                case "leverage":
                    self.__setattr__(key,int(query[key]))
                case "ticker":
                    self.__setattr__(key,str(query[key]))
                case "deadpoint":
                    self.__setattr__(key,float(query[key]))
                case "callback":
                    self.__setattr__(key,float(query[key]))
                case "strategy":
                    self.__setattr__(key,str(query[key]))

            