from coinbase.rest import RESTClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
from database.adatabase import ADatabase
import pandas as pd
from tqdm import tqdm
load_dotenv()
import os

key_id = os.getenv("SEANCOINBASEKEY")
private_key = os.getenv("SEANCOINBASESECRET")
api_key = f"organizations/{key_id}"
api_secret = f"-----BEGIN EC PRIVATE KEY-----\n{private_key}\n-----END EC PRIVATE KEY-----\n"

client = RESTClient(api_key,api_secret)
request_method = "GET"
request_path = "/api/v3/brokerage/accounts"
# jwt_uri = jwt_generator.format_jwt_uri(request_method, request_path)
# jwt_token = jwt_generator.build_rest_jwt(jwt_uri, api_key, api_secret)
# print(f"export JWT={jwt_token}")

market = ADatabase("market")

market.connect()
market.drop("xrp_futures")
for i in tqdm(range(768)):
    try:
        end_offset = i * 300
        start_offset = (i + 1) * 300
        start = datetime.now() - timedelta(minutes=start_offset)
        start_unix_timestamp = int(start.timestamp())
        end = datetime.now() - timedelta(minutes=end_offset)
        end_unix_timestamp = int(end.timestamp())
        ticker = "XRP-PERP-INTX"
        df = pd.DataFrame(client.get_candles(ticker,start_unix_timestamp,end_unix_timestamp,granularity="ONE_MINUTE")["candles"])
        df["ticker"] = ticker
        market.store("xrp_futures",df)
    except Exception as e:
        print(str(e))
market.disconnect()