from database.adatabase import ADatabase
from strategy.astrategy import AStrategy
from strategy.stratfact import StratFact
from checkpoint.modeler import Modeler
from checkpoint.transformer import Transformer
from checkpoint.backtester import Backtester
from checkpoint.analyzer import Analyzer
from tqdm import tqdm

class AProduct(AStrategy):

    def __init__(self,isai):
        self.strategies = []
        self.factors = []
        self.isai = isai

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
    
    def transform_strats(self):
        for strategy in self.strategies:
            Transformer.checkpoint(strategy)
    
    def model_strats(self):
        for strategy in self.strategies:
            Modeler.checkpoint(strategy)

    def model(self):
        Modeler.checkpoint(self)

    def transform(self):
        base_strat = self.strategies[0]
        base = base_strat.retrieve_simulation().rename(columns={"prediction":f"{base_strat.name}_prediction"})
        for strategy in self.strategies[1:]:
            try:
                sim = strategy.retrieve_simulation().rename(columns={"prediction":f"{strategy.name}_prediction"})
                self.factors.append(f"{strategy.name}_prediction")
                base = base_strat.processor.merge(base,sim,on=["year","quarter","month","week","date","ticker"])
            except:
                continue
        self.db.connect()
        self.drop_model_data()
        for ticker in tqdm(base["ticker"].unique(),desc="product data"):
            ticker_data = base[base["ticker"]==ticker].sort_values("date")
            ticker_data["prediction"] = 0
            for x in self.strategies:
                ticker_data["prediction"] = ticker_data["prediction"] + ticker_data[f"{x.name}_prediction"]
            ticker_data["prediction"] = ticker_data["prediction"] / len(self.strategies)
            ticker_data["y"] = ticker_data["adjclose"].shift(-self.parameter.holding_period)
            self.store_model_data(ticker_data)
        self.db.disconnect()
    
    def backtest(self):
        Backtester.checkpoint(self)
    
    def analyze(self):
        Analyzer.checkpoint(self)