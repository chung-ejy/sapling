from database.adatabase import ADatabase
from strategy.astrategy import AStrategy
from strategy.stratfact import StratFact
from checkpoint.modeler import Modeler
from checkpoint.transformer import Transformer
from checkpoint.backtester import Backtester
from checkpoint.analyzer import Analyzer

class AProduct(AStrategy):

    def __init__(self):
        self.strategies = []
    
    def build_strategies(self):
        for strategy_name in self.parameter.strategies:
            strategy = StratFact.factory(strategy_name)
            strategy.build(self.parameter)
            self.strategies.append(strategy)
            
    def init_name(self):
        names = [x.name for x in self.strategies]
        names.sort()
        self.name = "_".join(names)
        super().__init__(self.name)
        self.db = ADatabase(self.name)
    
    def transform(self):
        for strategy in self.strategies:
            Transformer.checkpoint(strategy)
    
    def model(self):
        for strategy in self.strategies:
            Modeler.checkpoint(strategy)

    def merge(self):
        base_strat = self.strategies[0]
        base = base_strat.retrieve_simulation().rename(columns={"prediction":f"{base_strat.name}_prediction"})
        for strategy in self.strategies[1:]:
            try:
                sim = strategy.retrieve_simulation().rename(columns={"prediction":f"{strategy.name}_prediction"})
                base = base_strat.processor.merge(base,sim,on=["year","quarter","month","week","date","ticker"])
            except:
                continue
        self.drop_simulation()
        self.store_simulation(base)
    
    def backtest(self):
        Backtester.checkpoint(self)
    
    def analyze(self):
        Analyzer.checkpoint(self)