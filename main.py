from backtest_functions.backtest_functions import BacktestFunctions as bf
from strategy.strategy import Strategy

for name in Strategy._member_names_:
    for i in range(60,65,5):
        for position in range(20,25,5):
            query = {
                "strategy":name,
                "holding_period":i,
                "positions":position,
                "stop_loss":0.03,
                "ascending":False,
            }
            results = bf.backtest(query)
            print(name,list(results.keys()))