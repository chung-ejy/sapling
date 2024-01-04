from backtest_functions.backtest_functions import BacktestFunctions as bf
from strategy.strategy import Strategy
import pandas as pd
from tqdm import tqdm

analysis = []
names = Strategy._member_names_
names = ["RF_ASSET_FACTOR_LOADING"]
for name in tqdm(names):
    for ascending in [False]:
        query = {
            "strategy":name,
            "holding_period":5,
            "positions":1,
            "stop_loss":0.03,
            "ascending":ascending,
        }
        results = bf.backtest(query)
        print(results["recommendations"])
        print(results["portfolio"][-1])
        print(results["trades"][-1])
        analysis.append({
            "strat":name,
            "cr":results["portfolio"][-1]["cumulative_return"]
        })
print(pd.DataFrame(analysis).sort_values("cr",ascending=False))