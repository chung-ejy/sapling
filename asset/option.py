import numpy as np
from scipy.stats import norm

class Option(object):

    @classmethod
    def black_scholes_call(self,S, K, T, r, sigma):
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return call_price
    
    @classmethod
    def black_scholes_put(self,S, K, T, r, sigma):
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return put_price
    
    @classmethod
    def update(self,row,asset):
        updated = asset.copy()
        updated["adjclose"] = row["adjclose"]
        updated["return"] = (updated["strike_price"] - row["adjclose"]) 
        updated["pv"] = max(0,updated["return"]) * updated["quantity"] + updated["notional"]
        return updated
    
    @classmethod
    def sell(self,row,asset):
        updated = asset.copy()
        updated["sell_date"] = row["date"]
        return updated
    
    @classmethod
    def buy(self,row,asset,notional):
        updated = asset.copy()
        updated["ticker"] = row["ticker"]
        updated["buy_date"] = row["date"]
        updated["strike_price"] = row["adjclose"] * (1.15)
        updated["premium"] = self.black_scholes_put(row["adjclose"],updated["strike_price"],float(0.25),row["rf"],row["sigma"])
        updated["contract_price"] = updated["strike_price"] + updated["premium"]
        updated["quantity"] = notional / (updated["contract_price"])
        updated["notional"] = notional 
        updated["pv"] = notional
        return updated