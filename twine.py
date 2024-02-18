from datetime import datetime, timedelta
from transformer.transformer import Transformer
from database.adatabase import ADatabase
from extractor.alp_client_extractor import ALPClientExtractor
from strategy.strategy_factory import StrategyFactory
from backtester.backtester import Backtester
from parameter.aparameter import AParameter
import pandas as pd

db = ADatabase("sapling")
today = datetime.now()
start = datetime.now() - timedelta(days=365.25)
end = datetime.now() - timedelta(hours=24)
db.cloud_connect()
bots = db.retrieve("bots")
keys = db.retrieve("secrets")
parameter = db.retrieve("kpi").sort_values("return",ascending=False).iloc[0].to_dict()
db.disconnect()

param = AParameter()
param.build(parameter)
sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",attrs={"id":"constituents"})[0].rename(columns={"Symbol":"ticker"})
param.tickers = list(sp500["ticker"].values)
strat = StrategyFactory.build(param)
sim = Transformer.transform(strat,start,end)
trades = Backtester.backtest(strat,sim)
recs = Backtester.recommendations(trades)

print(recs[["date","ticker","buy_date","sell_date"]].to_dict("records"))
for bot in bots.iterrows():
    try:
        user = bot[1]["username"]
        live = bot[1]["live"]
        user_keys = keys[keys["username"]==user].to_dict("records")[0]
        secret = user_keys["secret"]
        key = user_keys["key"]
        alp_client = ALPClientExtractor(key,secret)
        positions = recs.index.size
        account = alp_client.account()
        cash = float(account["cash"])
        notional = float(cash/positions)
        if live == True:
            if today.weekday() == 0:
                for row in recs.iterrows():
                    ticker = row[1]["ticker"]
                    alp_client.buy(ticker,notional)
            elif today.weekday() == 4:
                alp_client.close()
            else:
                continue
    except Exception as e:
        print(str(e))
        continue