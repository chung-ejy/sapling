from diversifier.adiversifier import ADiversifier
from database.adatabase import ADatabase

class Simple(ADiversifier):
    
    @classmethod
    def load(self):
        market = ADatabase("market")
        market.cloud_connect()
        categories = market.retrieve("sp500").rename(columns={"GICS Sector":"category"})
        categories["category"] = "simple"
        market.disconnect()
        return categories