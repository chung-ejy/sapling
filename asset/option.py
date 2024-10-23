import numpy as np
from scipy.stats import norm

class Option(object):

    def __init__(self,ticker="",adjclose=0,quantity=0):
        self.ticker = ticker
        self.adjclose = adjclose
        self.quantity = quantity
        
    def black_scholes_call(self,S, K, T, r, sigma):
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return call_price
    
    
    def black_scholes_put(self,S, K, T, r, sigma):
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return put_price
    
    def update(self, row):
        self.adjclose = row["adjclose"]
        
        # Intrinsic value of the put option: max(K - S, 0)
        self.option_return = max(self.strike_price - row["adjclose"], 0)
        
        # Present value (pv): Intrinsic value times quantity minus the total premium cost
        self.pv = (self.option_return * self.quantity) - (self.premium * self.quantity) + self.notional

    
    def buy(self,row,notional):
        self.ticker = row["ticker"]
        self.buy_date = row["date"]
        self.strike_price = row["adjclose"] * (0.95)
        self.premium = self.black_scholes_put(row["adjclose"],self.strike_price,float(0.25),row["rf"],row["sigma"])
        self.contract_price = self.strike_price + self.premium
        self.quantity = notional / (self.contract_price)
        self.notional = notional 
        self.pv = notional