
class Bond(object):

    @classmethod
    def update(self,row,asset):
        updated = asset.copy()
        return updated
    
    @classmethod
    def sell(self,row,asset):
        updated = asset.copy()
        updated["sell_date"] = row["date"]
        return updated
    
    @classmethod
    def buy(self,row,asset,notional):
        updated = asset.copy()
        updated["buy_date"] = row["date"]
        updated["sell_date"] = row["date"]
        updated["adjclose"] = 1000 / (1 + row["rf"])**10
        updated["quantity"] = notional / updated["adjclose"]
        updated["rate"] = row["rf"]
        updated["pv"] = updated["adjclose"] * updated["quantity"]
        return updated