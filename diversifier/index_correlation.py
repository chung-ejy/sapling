from diversifier.adiversifier import ADiversifier
from database.adatabase import ADatabase

class IndexCorrelation(ADiversifier):
    
    @classmethod
    def load(self):
        market = ADatabase("market")
        market.cloud_connect()
        categories = market.retrieve("spy_correlations").rename(columns={"correlation":"category"})
        market.disconnect()
        return categories