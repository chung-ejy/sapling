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

window = 10
time_between = 15
ticker_data = ALPPaperExtractor().crypto_prices(ticker,datetime.now()-timedelta(days=1),datetime.now())
ticker_data['rolling_mean'] = ticker_data['adjclose'].rolling(window=window).mean()
ticker_data['upper_band'] = ticker_data['rolling_mean'] + 2 * ticker_data['adjclose'].rolling(window=window).std()
ticker_data['lower_band'] = ticker_data['rolling_mean'] - 2 * ticker_data['adjclose'].rolling(window=window).std()
ticker_data['signal'] = 0
ticker_data['signal'][ticker_data['adjclose'] > ticker_data['upper_band']] = 1
ticker_data['signal'][ticker_data['adjclose'] < ticker_data['lower_band']] = -1 
current = ticker_data.iloc[-1]
signal = current["signal"]

for bot in bots.iterrows():
    try:
        user = bot[1]["username"]
        live = bot[1]["live"]
        user_keys = keys[keys["username"]==user].to_dict("records")[0]
        secret = user_keys["secret"]
        key = user_keys["key"]
        alp_client = ALPClientExtractor(key,secret)
        if live == True:
            if signal == 1:
                alp_client.close()
                cash = float(alp_client.account()["cash"])
                sleep(30)
                print(alp_client.buy(ticker,cash))
            elif signal == -1:
                alp_client.close()
                sleep(30)
                cash = float(alp_client.account()["cash"])
                print(alp_client.sell(ticker,cash))
            else:
                print(current["date"],"hold")
    except Exception as e:
        print(str(e))
        continue