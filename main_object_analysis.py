from strategy.magnificent_seven_quarterly import MagnificentSevenQuarterly
from strategy.financial_statement_quarterly import FinancialStatementQuarterly
from strategy.korean_tech_quarterly import KoreanTechQuarterly
from strategy.single_index_quarterly import SingleIndexQuarterly
from strategy.optimal_quarterly import OptimalQuarterly
from strategy.kr_financial_statement_yearly import KRFinancialStatementYearly
from processor.processor import Processor as processor
from database.adatabase import ADatabase
import numpy as np
import matplotlib.pyplot as plt

fred = ADatabase("fred")
fred.connect()

market_yield = fred.retrieve("market_yield")
market_yield = market_yield.rename(columns={"value":"rf"})
market_yield["rf"] = market_yield["rf"].replace(".",np.nan)
market_yield.dropna(inplace=True)
market_yield["rf"] = [float(x)/100 for x in market_yield["rf"]]
market_yield = processor.column_date_processing(market_yield)
spy = fred.retrieve("sp500")
spy = spy.rename(columns={"value":"spy"})
spy["spy"] = spy["spy"].replace(".",np.nan)
spy.dropna(inplace=True)
spy["spy"] = [float(x) for x in spy["spy"]]
spy = processor.column_date_processing(spy)
spy = spy.sort_values("date")
fred.disconnect()

strategies = [   
                KRFinancialStatementYearly()
              ,KoreanTechQuarterly()
              ,SingleIndexQuarterly()
              ,MagnificentSevenQuarterly()
              ,FinancialStatementQuarterly()

              ]


for strategy in strategies:
    try:
        strategy.db.connect()
        states = strategy.db.retrieve("states")
        trades = strategy.db.retrieve("trades")
        strategy.db.disconnect()
        visualization = states.merge(spy,on="date",how="left")
        visualization = visualization.merge(market_yield[["date","rf"]],on="date",how="left")
        visualization["return"] = (visualization["pv"] - visualization["pv"].iloc[0]) / visualization["pv"].iloc[0]
        visualization["benchmark_return"] = (visualization["spy"] - visualization["spy"].iloc[0]) / visualization["spy"].iloc[0]
        visualization["ir_return"] = (visualization["rf"] - visualization["rf"].iloc[0]) / visualization["rf"].iloc[0]
        # visualization["market_corr"] = visualization["return"].rolling(100).corr(visualization["benchmark_return"])
        # visualization["corr_return"] = (visualization["market_corr"] - visualization["market_corr"].iloc[0]) / visualization["market_corr"].iloc[0]
        visualization["sharpe_ratio"] = (visualization["return"] - visualization["benchmark_return"]) / visualization["return"].var()
        visualization["sharpe_return"] = (visualization["sharpe_ratio"] - visualization["sharpe_ratio"].iloc[1]) / visualization["sharpe_ratio"].iloc[1]
        # plt.plot(visualization["date"].values,visualization["return"])
        # plt.plot(visualization["date"].values,visualization["benchmark_return"])
        # plt.plot(visualization["date"].values,visualization["ir_return"])
        # plt.show()
        # print(states.iloc[-1]["stocks"])

        strategy.db.cloud_connect()
        strategy.db.drop("trades")
        strategy.db.drop("visualization")
        strategy.db.store("trades",trades)
        strategy.db.store("visualization",visualization.dropna())
        strategy.db.disconnect()
    except Exception as e:
        print(str(e))
        continue