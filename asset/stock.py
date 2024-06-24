
class Stock(object):

    @classmethod
    def update(self,row,asset):
        updated = asset.copy()
        updated["adjclose"] = row["adjclose"]
        # updated["returns"] = (updated["adjclose"] - updated["buy_price"]) / updated["buy_price"] 
        # updated["remaining_returns"] = updated["expected_return"] - updated["returns"]
        updated["expected_return"] = row["expected_return"]
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
        updated["type"] = row["type"]
        updated["expected_return"] = row["expected_return"]
        updated["adjclose"] = row["adjclose"]
        updated["buy_price"] = row["adjclose"]
        updated["buy_date"] = row["date"]
        updated["sell_date"] = row["date"]
        updated["quantity"] = notional / updated["adjclose"]
        updated["pv"] = updated["adjclose"] * updated["quantity"]
        return updated