from datetime import datetime, timedelta
from transformer.transformer import Transformer
from database.adatabase import ADatabase
from extractor.alp_extractor import ALPExtractor
from strategy.strategy_factory import StrategyFactory
from backtester.backtester import Backtester
from parameter.aparameter import AParameter
import pandas as pd

live = True
russell1000 = pd.read_html("https://en.wikipedia.org/wiki/Russell_1000_Index")[2].rename(columns={"Ticker":"ticker"})
alp = ALPExtractor()
today = datetime.now()
start = datetime.now() - timedelta(days=365.25*2)
end = datetime.now() - timedelta(hours=24)
param = AParameter()
param.tickers = russell1000["ticker"].values
strat = StrategyFactory.build(param)
sim = Transformer.cloud_transform(strat,start,end)
trades = Backtester.backtest(strat,sim)
recs = Backtester.recommendations(trades)

if today.weekday() == 0:
    positions = recs.index.size
    account = alp.account()
    cash = float(account["cash"])
    for row in recs.iterrows():
        ticker = row[1]["ticker"]
        date = row[1]["date"]
        price = round(row[1]["adjclose"],2)
        qty = int(cash/positions/price)
        print(date,ticker,price,qty)
        if live == True:
            alp.buy_stop_loss(ticker,price,qty)
if today.weekday() == 4:
    # alp.close()
    print("sell_day")