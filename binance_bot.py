from binance.um_futures import UMFutures
from database.adatabase import ADatabase
from binance_strategy.binance_strategy_factory import BinanceStrategyFactory
from crypto_parameter.acrypto_parameter import ACryptoParameter
from time import sleep

run = True
while run == True:
    db = ADatabase("sapling")
    db.cloud_connect()
    bots = db.retrieve("crypto_bots")
    keys = db.retrieve("crypto_secrets")
    parameters = db.retrieve("crypto_parameter")
    db.disconnect()
    for bot in bots.iterrows():
        user = bot[1]["username"]
        live = bot[1]["live"]
        if live == True:
            try:
                parameter = parameters[parameters["username"]==user].to_dict("records")[0]
                secret = keys[keys["username"]==user]["bsecret"].item()
                key = keys[keys["username"]==user]["bkey"].item()
                umf = UMFutures(key,secret)
                param = ACryptoParameter()
                param.build(parameter)
                binance_strategy = BinanceStrategyFactory.build(param)
                binance_strategy.load_umf(umf)
                binance_strategy.logic()
            except Exception as e:
                print(str(e))
            sleep(1)