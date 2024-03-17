from extractor.coinbase_client_extractor import CoinbaseClientExtractor
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta, timezone
import pandas as pd
import matplotlib.pyplot as plt
client = CoinbaseClientExtractor(os.getenv("SEANCOINBASEKEY"),os.getenv("SEANCOINBASESECRET"))

start = datetime.now() - timedelta(hours=5)
end = datetime.now()
start_utc = start.astimezone(timezone.utc)
start_unix_timestamp = (start_utc - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()

end_utc = end.astimezone(timezone.utc)
end_unix_timestamp = (end_utc - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()

df = pd.DataFrame(client.client.get_candles("BTC-USD",int(start.timestamp()),int(end.timestamp()),"ONE_MINUTE")["candles"]).sort_values("start")
df["close"] = [float(x) for x in df["close"]]
df["bollinger"] = df["close"].rolling(15).mean() + df["close"].rolling(15).std()
df["signal"] = df["bollinger"] > df["close"]
df["signal"] = [1 if x == True else - 1 for x in df["signal"]]
df["return"] = df["close"].pct_change(-5) * df["signal"] + 1
trades = df.iloc[::5]
trades["cr"] = trades["return"].cumprod()
print(trades.tail())