from backtest_functions.backtest_functions import BacktestFunctions as bf
from strategy.strategy import Strategy
import pandas as pd
from tqdm import tqdm

analysis = []
for name in tqdm(Strategy._member_names_):
    for ascending in [True,False]:
        query = {
            "strategy":name,
            "holding_period":5,
            "positions":10,
            "stop_loss":0.03,
            "ascending":ascending,
        }
        results = bf.backtest(query)
        analysis.append({
            "strat":name,
            "cr":results["portfolio"][-1]["cumulative_return"]
        })
print(pd.DataFrame(analysis).sort_values("cr",ascending=False))