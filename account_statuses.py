from datetime import datetime, timedelta
from database.adatabase import ADatabase
from extractor.alp_extractor import ALPExtractor
from extractor.alp_client_extractor import ALPClientExtractor

db = ADatabase("sapling")

alp = ALPExtractor()
today = datetime.now()
start = datetime.now() - timedelta(days=365.25*2)
end = datetime.now() - timedelta(hours=24)
db.cloud_connect()
bots = db.retrieve("bots")
keys = db.retrieve("secrets")
parameter = db.retrieve("kpi").sort_values("return",ascending=False).iloc[0].to_dict()
db.disconnect()

for bot in bots.iterrows():
    try:
        user = bot[1]["username"]
        live = bot[1]["live"]
        user_keys = keys[keys["username"]==user].to_dict("records")[0]
        secret = user_keys["secret"]
        key = user_keys["key"]
        alp_client = ALPClientExtractor(key,secret)
        account = alp_client.account()
        cash = float(account["cash"])
        print(cash)
    except Exception as e:
        print(str(e))
        continue