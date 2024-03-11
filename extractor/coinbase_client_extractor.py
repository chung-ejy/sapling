from coinbase.rest import RESTClient
from dotenv import load_dotenv
load_dotenv()
import os
import random
class CoinbaseClientExtractor(object):
    
    def __init__(self,key,secret):
        self.client = RESTClient(f"organizations/{key}",f"-----BEGIN EC PRIVATE KEY-----\n{secret}\n-----END EC PRIVATE KEY-----\n")

    def buy_stop_loss(self,ticker,notional,leverage):
        order_config = {
                "market_market_ioc": {
                "quote_size": str(notional)
                }
            }
        self.client.create_order(client_order_id="",product_id=ticker,side="BUY",order_configuration=order_config,leverage=leverage)
    
    def sell_stop_loss(self,ticker,notional,leverage):
        order_config = order_config = {
                "market_market_ioc": {
                "base_size": str(notional)
                }
            }
        self.client.create_order(client_order_id="",product_id=ticker,side="SELL",order_configuration=order_config,leverage=leverage)
        