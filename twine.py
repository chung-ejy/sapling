from datetime import datetime, timedelta
from transformer.transformer import Transformer
from database.adatabase import ADatabase
from extractor.alp_extractor import ALPExtractor
from extractor.alp_client_extractor import ALPClientExtractor
from strategy.strategy_factory import StrategyFactory
from backtester.backtester import Backtester
from parameter.aparameter import AParameter
import pandas as pd

db = ADatabase("sapling")



alp = ALPExtractor()
today = datetime.now()
start = datetime.now() - timedelta(days=365.25*2)
end = datetime.now() - timedelta(hours=24)
db.cloud_connect()
bots = db.retrieve("bots")
keys = db.retrieve("secrets")
parameter = db.retrieve("kpi").sort_values("return",ascending=False).iloc[0].to_dict()
db.disconnect()

if today.weekday() == 0:
    param = AParameter()
    param.build(parameter)
    sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",attrs={"id":"constituents"})[0].rename(columns={"Symbol":"ticker"})
    param.tickers = list(sp500["ticker"].values)
    strat = StrategyFactory.build(param)
    sim = Transformer.transform(strat,start,end)
    trades = Backtester.backtest(strat,sim)
    recs = Backtester.recommendations(trades)

    for bot in bots.iterrows():
        try:
            user = bot[1]["username"]
            live = bot[1]["live"]
            user_keys = keys[keys["username"]==user].to_dict("records")[0]
            secret = user_keys["secret"]
            key = user_keys["key"]
            alp_client = ALPClientExtractor(key,secret)
            positions = recs.index.size
            account = alp.account()
            cash = float(account["cash"])
            for row in recs.iterrows():
                ticker = row[1]["ticker"]
                price = round(row[1]["adjclose"],2)
                notional = int(cash/positions)
                if live == True:
                    alp_client.buy(ticker,notional)
        except Exception as e:
            print(str(e))
            continue

if today.weekday() == 4:
    for bot in bots.iterrows():
        try:
            user = bot[1]["username"]
            live = bot[1]["live"]
            user_keys = keys[keys["username"]==user].to_dict("records")[0]
            secret = user_keys["secret"]
            key = user_keys["key"]
            alp_client = ALPClientExtractor(key,secret)
            alp_client.close()
        except:
            continue