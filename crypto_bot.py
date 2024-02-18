from datetime import datetime, timedelta
from database.adatabase import ADatabase
from extractor.alp_client_extractor import ALPClientExtractor
from time import sleep
db = ADatabase("sapling")

db.cloud_connect()
bots = db.retrieve("bots").iloc[:1]
keys = db.retrieve("secrets")
db.disconnect()
ticker = "BTC/USD"

for bot in bots.iterrows():
    try:
        user = bot[1]["username"]
        live = bot[1]["live"]
        user_keys = keys[keys["username"]==user].to_dict("records")[0]
        secret = user_keys["secret"]
        key = user_keys["key"]
        if live == True:
            alp_client = ALPClientExtractor(key,secret)
            account = alp_client.account()
            cash = float(account["cash"])
            print(ticker,cash)      
    except Exception as e:
        print(str(e))
        continue