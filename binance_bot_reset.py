from datetime import datetime, timedelta
from binance.um_futures import UMFutures
from database.adatabase import ADatabase
from time import sleep
import pandas as pd
import random

db = ADatabase("sapling")
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
            umf = UMFutures(key,secret)
            account = umf.account()
            balances = pd.DataFrame(umf.balance())
            usdp_balance = balances[balances["asset"]=="USDT"]
            positions = pd.DataFrame(account["positions"])
            xrp_positions = positions[positions["symbol"]==ticker]
            cash = float(usdp_balance["balance"].item())
            columns = ["start","open","high","low","close","volumne","end","volume","trades","buy_volumne","base_volume","ignore"]
            df = pd.DataFrame(data=umf.klines(ticker,interval="1m"),columns=columns)
            df["date"] = [datetime.utcfromtimestamp(int(x/1000)) for x in df["start"]]
            df.sort_values("date",inplace=True)
            df["close"] = [float(x) for x in df["close"]]
            df["rolling"] = df["close"].rolling(band).mean()
            df["signal"] = df["rolling"] > df["close"]
            df["signal"] = [1 if x == True else -1 for x in df["signal"]]
            current_market = df.iloc[-1]
            signal = current_market["signal"].item()
            price = current_market["close"].item()
            quantity = round(float(cash*0.98/price)) * leverage
            pv = float(xrp_positions["notional"].item())
            starting_amount = xrp_positions["positionAmt"].item()
            breakevenPrice = xrp_positions["breakEvenPrice"].item()
            pnl = float(xrp_positions["unrealizedProfit"].item())
            umf.change_leverage(ticker,15)
            print(cash,quantity)
            if pnl != 0:
                umf.cancel_open_orders(ticker)
                if float(starting_amount) > 0:
                    umf.change_leverage(ticker,15)
                    print(umf.new_order(**
                        {
                            "side": "SELL",
                            "quantity":abs(float(starting_amount)),
                            "symbol": ticker,
                            "type": "MARKET",
                            "reduceOnly":True
                        }
                    ))
                else:
                    umf.change_leverage(ticker,15)
                    print(umf.new_order(**
                        {
                            "side": "BUY",
                            "quantity":abs(float(starting_amount)),
                            "symbol": ticker,
                            "type": "MARKET",
                            "reduceOnly":True
                        }
                    ))
        except Exception as e:
            print(str(e))