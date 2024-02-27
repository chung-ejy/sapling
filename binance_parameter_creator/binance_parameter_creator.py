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
                    "activationPrice":round(price*(1-profittake),4),
                    "callbackRate":float(callback),
                    "reduceOnly":True
                }
        return parameter
    
    @classmethod
    def long_stop_loss(self,ticker,quantity,price,stopPrice):
       parameter =  {
                        "side": "SELL",
                        "quantity":abs(float(quantity)),
                        "symbol": ticker,
                        "type": "STOP",
                        "price":float(price),
                        "stopPrice":round(stopPrice,4),
                        "reduceOnly":True
                    }
       return parameter
    
    @classmethod
    def short_stop_loss(self,ticker,quantity,price,stopPrice):
        parameter =  {
                        "side": "BUY",
                        "quantity":abs(float(quantity)),
                        "symbol": ticker,
                        "type": "STOP",
                        "price":float(price),
                        "stopPrice":round(stopPrice,4),
                        "reduceOnly":True
                    }
        return parameter
    
    @classmethod
    def long_limit_close(self,ticker,quantity,stopPrice):
       parameter =  {
                        "side": "SELL",
                        "quantity":abs(float(quantity)),
                        "symbol": ticker,
                        "type": "LIMIT",
                        "timeInForce":"GTC",
                        "price":round(float(stopPrice),4),
                        "reduceOnly":True
                    }
       return parameter
    
    @classmethod
    def short_limit_close(self,ticker,quantity,stopPrice):
        parameter =  {
                        "side": "BUY",
                        "quantity":abs(float(quantity)),
                        "symbol": ticker,
                        "type": "LIMIT",
                        "timeInForce":"GTC",
                        "price":round(float(stopPrice),4),
                        "reduceOnly":True
                    }
        return parameter
    
    @classmethod
    def long_take_profit(self,ticker,quantity,price,stopPrice):
       parameter =  {
                        "side": "SELL",
                        "quantity":abs(float(quantity)),
                        "symbol": ticker,
                        "type": "TAKE_PROFIT",
                        "price":float(price),
                        "stopPrice":round(stopPrice,4),
                        "reduceOnly":True
                    }
       return parameter
    
    @classmethod
    def short_take_profit(self,ticker,quantity,price,stopPrice):
        parameter =  {
                        "side": "BUY",
                        "quantity":abs(float(quantity)),
                        "symbol": ticker,
                        "type": "TAKE_PROFIT",
                        "price":float(price),
                        "stopPrice":round(stopPrice,4),
                        "reduceOnly":True
                    }
        return parameter

    @classmethod
    def long_stop_market(self,ticker,quantity,stopPrice):
       parameter =  {
                        "side": "SELL",
                        "quantity":abs(float(quantity)),
                        "symbol": ticker,
                        "type": "STOP_MARKET",
                        "stopPrice":round(stopPrice,4),
                        "reduceOnly":True
                    }
       return parameter
    
    @classmethod
    def short_stop_market(self,ticker,quantity,stopPrice):
        parameter =  {
                        "side": "BUY",
                        "quantity":abs(float(quantity)),
                        "symbol": ticker,
                        "type": "STOP_MARKET",
                        "stopPrice":round(stopPrice,4),
                        "reduceOnly":True
                    }
        return parameter

    