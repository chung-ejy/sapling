from extractor.coinbase_client_extractor import CoinbaseClientExtractor
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta, timezone
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from time import sleep
warnings.simplefilter(action="ignore")
client = CoinbaseClientExtractor(os.getenv("ERICCOINBASEKEY"),os.getenv("ERICCOINBASESECRET"))
tickers = ["BTC-USD","ETH-USD","SOL-USD","XRP-USD","AVAX-USD","ADA-USD"]
cash = 100
rolling_val = 60
holding_period = 5
while True:
    try:
        start = datetime.now() - timedelta(hours=5)
        end = datetime.now()
        start_utc = start.astimezone(timezone.utc)
        accounts = pd.DataFrame(client.client.get_accounts()["accounts"])
        accounts["balance"] = [float(row[1]["available_balance"]["value"]) for row in accounts.iterrows()]
        cash_account = accounts[accounts["currency"]=="USD"]
        crypto_account = accounts.sort_values("balance",ascending=False).head(1)
        cash = float(cash_account["balance"].item())
        crypto = float(crypto_account["balance"].item())
        currency = crypto_account["currency"].item()
        end_utc = end.astimezone(timezone.utc)
        fills = client.client.get_fills()["fills"]
        prices = []
        for ticker in tickers:
            try:
                df = pd.DataFrame(client.client.get_candles(ticker,int(start_utc.timestamp()),int(end_utc.timestamp()),"ONE_MINUTE")["candles"]).sort_values("start")
                df["close"] = [float(x) for x in df["close"]]
                # df["signal"] = df["close"].rolling(rolling_val).std() / df["close"].rolling(rolling_val).mean()
                df["signal"] = df["close"].pct_change(holding_period).rolling(rolling_val).mean()
                df["return"] = df["close"].pct_change(-holding_period) + 1
                df["ticker"] = ticker
                prices.append(df)
            except Exception as e:
                print(ticker,str(e))
        sim = pd.concat(prices)
        trades = sim.iloc[::holding_period].sort_values("signal",ascending=False).groupby("start").first()
        trades["cr"] = trades["return"].cumprod()
        recommendation = trades.tail(1)
        print("sell")
        print("buy",recommendation["ticker"].item()+"-"+currency,cash)
    except Exception as e:
        print(str(e))
    sleep(60*holding_period)
