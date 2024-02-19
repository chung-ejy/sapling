from coinbase.rest import RESTClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
from database.adatabase import ADatabase
import pandas as pd
from tqdm import tqdm
load_dotenv()

org_id = ""
key_id = ""
private_key = ""
api_key = "organizations/3acf215e-8e7c-4e6c-a455-bfd9ec511a40/apiKeys/e66319db-0bdc-4bea-9bc4-6957ea875eea"
api_secret = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIE2TF1X/79ieqXGxIlnePDpy4a0sB9pOMYdR0yKfmk2doAoGCCqGSM49\nAwEHoUQDQgAE0J9DgBzqEGtC40yxR9Vy3KTzDwHiuuSnzX4Zt0pcc+9iASmWEPYc\nb8NSwFHB1s46C78wKmkJCFvwtPpYStQwiQ==\n-----END EC PRIVATE KEY-----\n"

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