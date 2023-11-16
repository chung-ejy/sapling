from datetime import datetime, timedelta
from database.adatabase import ADatabase

class AStrategy(object):

    def __init__(self,name,cycle):
        self.name = name
        self.cycle = cycle
        self.today = datetime.now()
        self.extraction_date = self.today - timedelta(days=self.cycle*2) - timedelta(days=140)
        self.model_start = self.today - timedelta(days=self.cycle*2)
        self.model_end = self.today - timedelta(days=self.cycle)
        self.backtest_start = self.model_end
        self.backtest_end = self.today

        self.db = ADatabase(self.name)
        self.model_data_table = "model_data"
        self.historical_model_table = "historical_model"
        self.simulation_table = "simulation"
        self.trades_table = "trades"
        self.portfolio_table = "portfolio"
        self.current_model_table = "current_model"
        self.recommendation_table = "recommendation"

    def store_model_data(self,model_data):
        self.db.connect()
        self.db.store(self.model_data_table,model_data)
        self.db.disconnect()
    
    def retrieve_model_data(self):
        self.db.connect()
        collections = self.db.retrieve(self.model_data_table)
        self.db.disconnect()
        return collections
    
    def drop_model_data(self):
        self.db.connect()
        self.db.drop(self.model_data_table)
        self.db.disconnect()
    
    def store_historical_model(self,historical_model):
        self.db.connect()
        self.db.store(self.historical_model_table,historical_model)
        self.db.disconnect()
    
    def retrieve_historical_model(self):
        self.db.connect()
        collections = self.db.retrieve(self.historical_model_table)
        self.db.disconnect()
        return collections
    
    def drop_historical_model(self):
        self.db.connect()
        self.db.drop(self.historical_model_table)
        self.db.disconnect()
    
    def store_simulation(self,simulation):
        self.db.connect()
        self.db.store(self.simulation_table,simulation)
        self.db.disconnect()
    
    def retrieve_simulation(self):
        self.db.connect()
        collections = self.db.retrieve(self.simulation_table)
        self.db.disconnect()
        return collections
    
    def drop_simulation(self):
        self.db.connect()
        self.db.drop(self.simulation_table)
        self.db.disconnect()
    
    def store_trades(self,trades):
        self.db.connect()
        self.db.store(self.trades_table,trades)
        self.db.disconnect()
    
    def retrieve_trades(self):
        self.db.connect()
        collections = self.db.retrieve(self.trades_table)
        self.db.disconnect()
        return collections
    
    def drop_trades(self):
        self.db.connect()
        self.db.drop(self.trades_table)
        self.db.disconnect()
    
    def store_portfolio(self,portfolio):
        self.db.connect()
        self.db.store(self.portfolio_table,portfolio)
        self.db.disconnect()
    
    def retrieve_portfolio(self):
        self.db.connect()
        collections = self.db.retrieve(self.portfolio_table)
        self.db.disconnect()
        return collections
    
    def drop_portfolio(self):
        self.db.connect()
        self.db.drop(self.portfolio_table)
        self.db.disconnect()
    
    def store_current_model(self,current_model):
        self.db.connect()
        self.db.store(self.current_model_table,current_model)
        self.db.disconnect()
    
    def retrieve_current_model(self):
        self.db.connect()
        collections = self.db.retrieve(self.current_model_table)
        self.db.disconnect()
        return collections
    
    def drop_current_model(self):
        self.db.connect()
        self.db.drop(self.current_model_table)
        self.db.disconnect()
    
    def store_recommendation(self,recommendation):
        self.db.connect()
        self.db.store(self.recommendation_table,recommendation)
        self.db.disconnect()
    
    def retrieve_recommendation(self):
        self.db.connect()
        collections = self.db.retrieve(self.recommendation_table)
        self.db.disconnect()
        return collections
    
    def drop_recommendation(self):
        self.db.connect()
        self.db.drop(self.recommendation_table)
        self.db.disconnect()