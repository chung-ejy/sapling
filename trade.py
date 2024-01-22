from datetime import datetime
from database.adatabase import ADatabase
from extractor.alp_extractor import ALPExtractor as alp

live = False
today = datetime.now()
db = ADatabase("sapling")
db.connect()
recs = db.retrieve("recommendations")
db.disconnect()

positions = recs.index.size
account = alp.account()
cash = float(account["cash"])
for row in recs.iterrows():
    ticker = row[1]["ticker"]
    price = round(row[1]["adjclose"],2)
    qty = int(cash/positions/price)
    print(ticker,price,qty)
    if live == True:
        alp.buy_stop_loss(ticker,price,qty)