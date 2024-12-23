from strategy.single_index_quarterly import SingleIndexQuarterly
from asset.stock import Stock
from data.market_data import MarketData
from asset.exposure import Exposure
from datetime import datetime
import unittest

class TestSingleIndexQuarterly(unittest.TestCase):

    def setUp(self):
        self.strategy = SingleIndexQuarterly()

    def test_sell_clause(self):
        true_stock = Stock("","",0,0,datetime(2020,1,1),Exposure.LONG)
        false_stock = Stock("","",0,0,datetime(2020,4,1),Exposure.LONG)
        market_data = MarketData(datetime(2020,4,1),"",0,0,Exposure.LONG,0)
        self.assertEquals(self.strategy.sell_clause(true_stock,market_data),True)
        self.assertEquals(self.strategy.sell_clause(false_stock,market_data),False)
    
    def test_update(self):
        true_stock = Stock("","",0,0,datetime(2020,1,1),Exposure.LONG)
        new_stock = Stock("","",0,0,datetime(2020,1,1),Exposure.LONG)
        market_data = MarketData(datetime(2020,4,1),"",1,0,Exposure.LONG,0)
        self.strategy.update(true_stock,market_data)
        self.assertNotEquals(true_stock.adjclose,new_stock.adjclose)
        self.assertNotEquals(true_stock.date,new_stock.date)
        self.assertEquals(true_stock.purchase_date,new_stock.purchase_date)
        self.assertEquals(true_stock.purchase_price,new_stock.purchase_price)