from datetime import datetime, timedelta
from binance.cm_futures import CMFutures
from database.adatabase import ADatabase
from time import sleep
import pandas as pd
import random

db = ADatabase("sapling")
cm_futures_client = CMFutures()
while True:
    db.cloud_connect()
    bots = db.retrieve("crypto_bots")
    keys = db.retrieve("crypto_secrets")
    parameter = db.retrieve("crypto_parameter")
    db.disconnect()
    ticker = parameter["ticker"].item()
    band = parameter["band"].item()
    stoploss = parameter["stoploss"].item()
    profittake = parameter["profittake"].item()
    leverage = parameter["leverage"].item()
    for bot in bots.iterrows():
        user = bot[1]["username"]
        live = bot[1]["live"]
        if live == True:
            try:
                secret = keys[keys["username"]==user]["bsecret"].item()
                key = keys[keys["username"]==user]["bkey"].item()
                cce = CMFutures(key,secret)
                print(cce.account())
                columns = ["start","open","high","low","close","volumne","end","volume","trades","buy_volumne","base_volume","ignore"]
                df = pd.DataFrame(data=cce.klines("XRPUSD_PERP",interval="1m"),columns=columns)
                df["date"] = [datetime.utcfromtimestamp(int(x/1000)) for x in df["start"]]
                df.sort_values("date",inplace=True)
                df["close"] = [float(x) for x in df["close"]]
                df["rolling"] = df["close"].rolling(band).mean()
                df["signal"] = df["rolling"] > df["close"]
                df["signal"] = [1 if x == True else - 1 for x in df["signal"]]
                current_market = df.iloc[-1]
                print(current_market)
                signal = current_market["signal"].item()
                # if True:
                #     if signal == 1:
                #         cce.
                #     elif signal == -1:
            except Exception as e:
                print(str(e))
            sleep(30)