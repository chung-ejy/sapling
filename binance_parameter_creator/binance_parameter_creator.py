

class BinanceParameterCreator(object):

    @classmethod
    def long_market_open(self,ticker,quantity):
        parameter = {
                "side": "BUY",
                "quantity":abs(float(quantity)),
                "symbol": ticker,
                "type":"MARKET"
            }
        return parameter
    
    @classmethod
    def short_market_open(self,ticker,quantity):
        parameter = {
                "side": "SELL",
                "quantity":abs(float(quantity)),
                "symbol": ticker,
                "type":"MARKET"
                
            }
        return parameter
    
    @classmethod
    def long_market_close(self,ticker,quantity):
        parameter = {
                "side": "SELL",
                "quantity":abs(float(quantity)),
                "symbol": ticker,
                "type":"MARKET",
                "reduceOnly":True
            }
        return parameter
    
    @classmethod
    def short_market_close(self,ticker,quantity):
        parameter = {
                "side": "BUY",
                "quantity":abs(float(quantity)),
                "symbol": ticker,
                "type":"MARKET",
                "reduceOnly":True
            }
        return parameter
    
    @classmethod
    def long_trailing_stop(self,ticker,quantity,price,profittake,callback):
        parameter = {
            "side": "SELL",
            "quantity":abs(float(quantity)),
            "symbol": ticker,
            "type": "TRAILING_STOP_MARKET",
            "activationPrice":round(price*(1+profittake),4),
            "callbackRate":float(callback),
            "reduceOnly":True
        }
        return parameter
    
    @classmethod
    def short_trailing_stop(self,ticker,quantity,price,profittake,callback):
        parameter = {
                    "side": "BUY",
                    "quantity":abs(float(quantity)),
                    "symbol": ticker,
                    "type": "TRAILING_STOP_MARKET",
                    "activationPrice":round(price * (1-profittake),4),
                    "callbackRate":float(callback),
                    "reduceOnly":True
                }
        return parameter
    
    @classmethod
    def long_stop_loss(self,ticker,quantity,price,stoploss):
       parameter =  {
                        "side": "SELL",
                        "quantity":abs(float(quantity)),
                        "symbol": ticker,
                        "type": "STOP",
                        "price":float(price),
                        "stopPrice":round(price*(1-stoploss),4),
                        "reduceOnly":True
                    }
       return parameter
    
    @classmethod
    def short_stop_loss(self,ticker,quantity,price,stoploss):
        parameter =  {
                        "side": "BUY",
                        "quantity":abs(float(quantity)),
                        "symbol": ticker,
                        "type": "STOP",
                        "price":float(price),
                        "stopPrice":round(price*(1+stoploss),4),
                        "reduceOnly":True
                    }
        return parameter

    