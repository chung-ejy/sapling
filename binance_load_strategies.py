import pandas as pd
from database.adatabase import ADatabase
from binance_strategy.binance_strategy import BinanceStrategy

db = ADatabase("sapling")
db.cloud_connect()
db.drop("crypto_strategies")
db.store("crypto_strategies",pd.DataFrame({"strategies":[x.value for x in BinanceStrategy]}))
db.disconnect()