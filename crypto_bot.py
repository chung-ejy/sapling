from datetime import datetime, timedelta
from database.adatabase import ADatabase
from extractor.alp_client_extractor import ALPClientExtractor
from extractor.alp_paper_extractor import ALPPaperExtractor
from time import sleep

db = ADatabase("sapling")
db.cloud_connect()
bots = db.retrieve("bots").iloc[:1]
keys = db.retrieve("secrets")
db.disconnect()
ticker = "BTC/USD"
rolling = 30 
time_between = 15
for bot in bots.iterrows():
    try:
        user = bot[1]["username"]
        live = bot[1]["live"]
        user_keys = keys[keys["username"]==user].to_dict("records")[0]
        secret = user_keys["secret"]
        key = user_keys["key"]
        alp_client = ALPClientExtractor(key,secret)
        if live == True:
            buy_price = 0
            sell_price = 0
            while True:
                ##close
                ticker_data = ALPPaperExtractor().crypto_prices(ticker,datetime.now()-timedelta(days=1),datetime.now())
                sell_price = ticker_data.iloc[0]["adjclose"]
                print(datetime.now(),buy_price-sell_price,"sell")
                ticker_data["intrinsic"] = ticker_data["adjclose"].rolling(30).mean() - 2 * ticker_data["adjclose"].rolling(rolling).std()
                ticker_data["signal"] = ticker_data["intrinsic"] < ticker_data["adjclose"]
                current = ticker_data.iloc[-1]
                signal = current["signal"]
                if signal == True:
                    buy_price = current["adjclose"]
                    print(datetime.now(),buy_price,"buy")
                else:
                    print(current["intrinsic",current["adjclose"]])
                sleep(60*time_between)
                # account = alp_client.account()
                # cash = float(account["cash"])
    except Exception as e:
        print(str(e))
        continue