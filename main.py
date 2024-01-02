from backtest_functions.backtest_functions import BacktestFunctions as bf

query = {
    "strategy":"KURTOSIS",
    "holding_period":5,
    "positions":10,
    "stop_loss":0.03,
    "ascending":False,
}

results = bf.backtest(query)
print(results["portfolio"][::10])