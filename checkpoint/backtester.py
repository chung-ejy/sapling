import pandas as pd
from tqdm import tqdm

class Backtester(object):
   
    @classmethod 
    def checkpoint(self,product):
        product.fed.connect()
        benchmark = product.processor.column_date_processing(product.fed.retrieve("sp500")).rename(columns={"value":"sp500"})
        yields = product.processor.column_date_processing(product.fed.retrieve("tyields")).rename(columns={"value":"yield1"})
        yields["yield1"] = [float(x)/100 for x in yields["yield1"]]
        sp500_projections = product.fed.retrieve("sp500_v2_projections").rename(columns={"prediction":"sp500_prediction"})
        product.fed.disconnect()
    
        simulation = product.retrieve_simulation()
        simulation = product.processor.column_date_processing(simulation)
        product.market.connect()
        sp100 = product.market.retrieve("sp100")
        product.market.disconnect()
        simulation = product.processor.merge(simulation,sp100,on="ticker")
        simulation = product.processor.merge(simulation,sp500_projections,on=["year","quarter"])
        simulation = product.processor.merge(simulation,benchmark,on="date")
        simulation = product.processor.merge(simulation,yields,on="date").ffill().bfill()
        bt_data = []

        for ticker in tqdm(simulation["ticker"].unique(),desc="backtest_prep"):
            prices = simulation[simulation["ticker"]==ticker]
            prices.sort_values("date",inplace=True)
            # for strategy in product.strategies:
            #     strategy_name = strategy.name
            #     prices[f"{strategy_name}_signal"] = (prices[f"{strategy_name}_prediction"] - prices["adjclose"]) / prices["adjclose"]
            prices["signal"] = (prices["prediction"] - prices["adjclose"]) / prices["adjclose"]
            prices["std"] = prices["adjclose"].rolling(product.parameter.holding_period).std()
            prices["rolling"] = prices["adjclose"].rolling(product.parameter.holding_period).mean()
            prices["risk"] = prices["std"] / prices["rolling"]
            prices["sell_price"] = prices["adjclose"].shift(-product.parameter.holding_period)
            prices["sell_date"] = prices["date"].shift(-product.parameter.holding_period)
            bt_data.append(prices.dropna())
        sim = pd.concat(bt_data)

        # sim["signal"] = 0
        # for x in product.strategies:
        #     sim["signal"] = sim["signal"] + sim[f"{x.name}_signal"]
        # sim["signal"] = sim["signal"] / len(product.strategies)

        if product.parameter.cfa == True:
            sim["sp500_var"] = sim["sp500"].rolling(50).var()
            sim["sp500_cov"] = sim["sp500"].rolling(50).cov(sim["adjclose"].rolling(50).mean())
            sim["market_return"] = (sim["sp500"].shift(-262) - sim["sp500"]) / sim["sp500"]
            sim["market_expected_return"] = (sim["sp500_prediction"] - sim["sp500"]) / sim["sp500"]
            sim["beta"] = sim["sp500_cov"] / sim["sp500_var"]
            sim["signal"] = (sim["signal"]) - sim["yield1"] + sim["beta"] * (sim["market_expected_return"]-sim["yield1"])
            sim["abs"] = sim["signal"].abs()
            sim["direction"] = sim["signal"] / sim["abs"]
        else:
            sim["abs"] = sim["signal"].abs()
            sim["direction"] = sim["signal"] / sim["abs"]
        
        positions = 10 if product.parameter.industry_diversified == False else len(simulation["GICS Sector"].unique())
        sim["return"] = (sim["sell_price"] - sim["adjclose"]) / sim ["adjclose"] * (1/positions) * sim["direction"]
        sim.sort_values("date",inplace=True)
        
        trades = sim[sim["weekday"]==4]
        trades = trades[trades["abs"]>=product.parameter.rr]
        trades = trades[trades["risk"]<=product.parameter.risk]
        week_mod = int(product.parameter.holding_period / 5)
        trades = trades[trades["week"] % week_mod + 1 == 1]
        if product.parameter.industry_diversified:
            trades = trades.sort_values("abs").groupby(["date","GICS Sector"]).first().reset_index()
        else:
            trades = trades.sort_values("abs").groupby(["date"]).nth([i for i in range(positions)])
        product.drop_trades()
        product.store_trades(trades)
