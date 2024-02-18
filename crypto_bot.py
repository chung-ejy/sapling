from datetime import datetime, timedelta
from database.adatabase import ADatabase
from extractor.alp_client_extractor import ALPClientExtractor
from extractor.alp_paper_extractor import ALPPaperExtractor
from time import sleep
import warnings
warnings.simplefilter("ignore")

db = ADatabase("sapling")
db.cloud_connect()
bots = db.retrieve("crypto_bots")
keys = db.retrieve("secrets")
db.disconnect()
ticker = "BTC/USD"

window = 30  # You can adjust this value based on your strategy
ticker_data = ALPPaperExtractor().crypto_prices(ticker,datetime.now()-timedelta(days=1),datetime.now())
ticker_data['rolling_mean'] = ticker_data['adjclose'].rolling(window=window).mean()
ticker_data["signal"] = ticker_data["rolling_mean"] > ticker_data["adjclose"]
current = ticker_data.iloc[-1]
signal = current["signal"]
print(current)
for bot in bots.iterrows():
    try:
        user = bot[1]["username"]
        live = bot[1]["live"]
        user_keys = keys[keys["username"]==user].to_dict("records")[0]
        secret = user_keys["secret"]
        key = user_keys["key"]
        alp_client = ALPClientExtractor(key,secret)
        if live == True:
            alp_client.close()
            sleep(60)
            if signal == True:
                cash = float(alp_client.account()["cash"])
                alp_client.buy(ticker,cash)
    except Exception as e:
        print(str(e))
        continue