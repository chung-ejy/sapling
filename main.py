from backtest_functions.backtest_functions import BacktestFunctions as bf

query = {
    "strategy":"HISTORICAL_VOLATILITY",
    "holding_period":5,
    "positions":5,
    "stop_loss":0.5,
}

results = bf.backtest(query)
print(results["portfolio"][::10])