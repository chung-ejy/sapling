from datetime import datetime, timedelta
from extractor.coinbase_client_extractor import CoinbaseClientExtractor
from database.adatabase import ADatabase
from time import sleep
import pandas as pd
import random
import math
db = ADatabase("sapling")


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
                secret = keys[keys["username"]==user]["secret"].item()
                key = keys[keys["username"]==user]["key"].item()
                cce = CoinbaseClientExtractor(key,secret)
                portfolios = pd.DataFrame(cce.client.get_portfolios()["portfolios"])
                perpetual_uuid = portfolios[portfolios["name"]=="Perpetuals"]["uuid"].item()
                perp_portfolio = cce.client.get_portfolio_breakdown(portfolio_uuid=perpetual_uuid)["breakdown"]
                balances = perp_portfolio["portfolio_balances"]
                cash_balances = balances["total_cash_equivalent_balance"]
                cash = float(cash_balances["value"])
                perps = pd.DataFrame(perp_portfolio["perp_positions"])
                date = datetime.now()
                start = datetime.now() - timedelta(minutes=300)
                start_unix_timestamp = int(start.timestamp())
                end = datetime.now()
                end_unix_timestamp = int(end.timestamp())
                df = pd.DataFrame(cce.client.get_candles(ticker,start_unix_timestamp,end_unix_timestamp,granularity="ONE_MINUTE")["candles"])
                df["date"] = [datetime.utcfromtimestamp(int(x)) for x in df["start"]]
                df.sort_values("date",inplace=True)
                df["close"] = [float(x) for x in df["close"]]
                df["rolling"] = df["close"].rolling(band).mean()
                df["signal"] = df["rolling"] > df["close"]
                df["signal"] = [1 if x == True else - 1 for x in df["signal"]]
                current_market = df.iloc[-1]
                signal = current_market["signal"].item()
                price = current_market["close"].item()
                size = round(float(cash/price),2)
                if perps.index.size == 0:
                    if signal == 1:
                        print(cce.client.market_order_buy(client_order_id=str(random.randint(0,100000000)),product_id=ticker,quote_size=str(cash)
                                                           ,leverage=str(leverage),retail_portfolio_id=perpetual_uuid))
                    elif signal == -1:
                        print(cce.client.market_order_sell(client_order_id=str(random.randint(0,100000000)),product_id=ticker,base_size=str(cash)
                                                           ,leverage=str(leverage),retail_portfolio_id=perpetual_uuid))
                else:
                    current_position = perps.iloc[0]
                    side = current_position["position_side"]
                    product_id = current_position["product_id"]
                    pnl = float(current_position["unrealized_pnl"]["userNativeCurrency"]["value"])
                    mark_price = float(current_position["mark_price"]["userNativeCurrency"]["value"])
                    net_size = float(current_position["net_size"])
                    buy_notional = mark_price * net_size
                    percent_pnl = float(pnl/buy_notional)
                    sell_notional = float(current_position["vwap"]["userNativeCurrency"]["value"])
                    if side == "POSITION_SIDE_BUY":
                        if percent_pnl > profittake or percent_pnl < -stoploss:
                            print(cce.client.create_order(client_order_id=str(random.randint(0,100000000)),product_id=ticker,side="SELL",order_configuration={
                                "market_market_ioc": {
                                    "quote_size": str(sell_notional)
                                    }
                            },leverage=str(leverage),margin_type="CROSS",retail_portfolio_id=perpetual_uuid))
                    else:
                        if percent_pnl < -profittake or percent_pnl > stoploss:
                            print(cce.client.create_order(client_order_id=str(random.randint(0,100000000)),product_id=ticker,side="BUY",order_configuration={
                                "market_market_ioc": {
                                    "base_size": str(sell_notional)
                                    }
                            },leverage=str(leverage),margin_type="CROSS",retail_portfolio_id=perpetual_uuid))
            except Exception as e:
                print(str(e))
            sleep(30)