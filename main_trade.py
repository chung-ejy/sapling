from database.adatabase import ADatabase
from extractor.alp_extractor import ALPExtractor

alp = ALPExtractor()
db = ADatabase("algo")
db.connect()
recs = db.retrieve("recommendations")
db.disconnect()

positions = recs.index.size
account = alp.account()
cash = float(account["cash"])
for row in recs.iterrows():
    ticker = row[1]["ticker"]
    price = round(row[1]["adjclose"],2)
    direction = row[1]["direction"]
    qty = int(cash/positions/price)
    if direction == 1:
        # alp.buy(ticker,qty)
        print("long",ticker,price,qty)
    else:
        # alp.sell(ticker,qty)
        print("short",ticker,price,qty)

