
class Stock(object):

    @classmethod
    def update(self,row,asset):
        updated = asset.copy()
        updated["adjclose"] = row["adjclose"]
        updated["pv"] = updated["adjclose"] * updated["quantity"]
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
        updated["adjclose"] = row["adjclose"]
        updated["buy_price"] = row["adjclose"]
        updated["buy_date"] = row["date"]
        updated["sell_date"] = None
        updated["quantity"] = notional / updated["adjclose"]
        updated["pv"] = updated["adjclose"] * updated["quantity"]
        return updated