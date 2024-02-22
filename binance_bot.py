from datetime import datetime, timedelta
from binance.cm_futures import CMFutures
from binance.um_futures import UMFutures
from database.adatabase import ADatabase
from time import sleep
import pandas as pd
import random

while True:
    db = ADatabase("sapling")
    db.cloud_connect()
    bots = db.retrieve("crypto_bots")
    keys = db.retrieve("crypto_secrets")
    parameter = db.retrieve("crypto_parameter")
    db.disconnect()
    ticker = parameter["ticker"].item()
    ticker = "XRPUSD_PERP"
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
                cmf = CMFutures(key,secret)
                umf = UMFutures(key,secret)
                account = cmf.account()
                balances = pd.DataFrame(umf.balance())
                usdp_balance = balances[balances["asset"]=="USDP"]
                positions = pd.DataFrame(account["positions"])
                xrp_positions = positions[positions["symbol"]=="XRPUSD_PERP"]
                print(xrp_positions)
                print(usdp_balance.columns)
                cash = float(usdp_balance["balance"].item())
                columns = ["start","open","high","low","close","volumne","end","volume","trades","buy_volumne","base_volume","ignore"]
                df = pd.DataFrame(data=cmf.klines("XRPUSD_PERP",interval="1m"),columns=columns)
                df["date"] = [datetime.utcfromtimestamp(int(x/1000)) for x in df["start"]]
                df.sort_values("date",inplace=True)
                df["close"] = [float(x) for x in df["close"]]
                df["rolling"] = df["close"].rolling(band).mean()
                df["signal"] = df["rolling"] > df["close"]
                df["signal"] = [1 if x == True else - 1 for x in df["signal"]]
                current_market = df.iloc[-1]
                print(current_market)
                signal = current_market["signal"].item()
                price = current_market["close"].item()
                # quantity = round(float(cash*0.98/price))
                quantity = 1
                print(quantity)
                if cash != 0:
                    print(cmf.cancel_open_orders("XRPUSD_PERP"))
                    if signal == 1:
                        ## market order
                        print(cmf.new_order(**
                            {
                                "side": "BUY",
                                "quantity":quantity,
                                "symbol": "XRPUSD_PERP",
                                "type": "MARKET",
                                "leverage":leverage
                            }
                        ))
                        print(cmf.new_order(**
                            {
                                "reduceOnly": True,
                                "side": "SELL",
                                "stopPrice":round(price*(1+profittake),4),
                                "quantity":quantity,
                                "symbol": "XRPUSD_PERP",
                                "timeInForce": "GTC",
                                "type": "TAKE_PROFIT",
                                "leverage":leverage
                            }
                        ))
                        print(cmf.new_order(**
                            {
                                "reduceOnly": True,
                                "side": "SELL",
                                "stopPrice":round(price*(1-stoploss),4),
                                "quantity":quantity,
                                "symbol": "XRPUSD_PERP",
                                "timeInForce": "GTC",
                                "type": "STOP",
                                "leverage":leverage
                            }
                        ))
                    elif signal == -1:
                        print(cmf.new_order(**
                            {
                                "side": "SELL",
                                "quantity":quantity,
                                "symbol": "XRPUSD_PERP",
                                "type": "MARKET",
                                "leverage":leverage
                            }
                        ))
                        print(cmf.new_order(**
                            {
                                "reduceOnly": True,
                                "side": "BUY",
                                "stopPrice":round(price*(1-profittake),4),
                                "quantity":quantity,
                                "symbol": "XRPUSD_PERP",
                                "timeInForce": "GTC",
                                "type": "TAKE_PROFIT",
                                "leverage":leverage
                            }
                        ))
                        print(cmf.new_order(**
                            {
                                "reduceOnly": True,
                                "side": "BUY",
                                "stopPrice":round(price*(1+stoploss),4),
                                "quantity":quantity,
                                "symbol": "XRPUSD_PERP",
                                "timeInForce": "GTC",
                                "type": "STOP",
                                "leverage":leverage
                            }
                        ))
                else:
                    print("waiting on positions")
            except Exception as e:
                print(str(e))
            sleep(1)