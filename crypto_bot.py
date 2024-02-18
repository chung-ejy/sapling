from datetime import datetime, timedelta
from database.adatabase import ADatabase
from extractor.alp_client_extractor import ALPClientExtractor
from extractor.alp_paper_extractor import ALPPaperExtractor
from time import sleep
import warnings
warnings.simplefilter("ignore")

db = ADatabase("sapling")
db.cloud_connect()
bots = db.retrieve("bots").iloc[:1]
keys = db.retrieve("secrets")
db.disconnect()
ticker = "BTC/USD"

window = 10  # You can adjust this value based on your strategy
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
            cash = 55000
            while True:
                ##close
                ticker_data = ALPPaperExtractor().crypto_prices(ticker,datetime.now()-timedelta(days=1),datetime.now())
                ticker_data['rolling_mean'] = ticker_data['adjclose'].rolling(window=window).mean()
                ticker_data['upper_band'] = ticker_data['rolling_mean'] + 2 * ticker_data['adjclose'].rolling(window=window).std()
                ticker_data['lower_band'] = ticker_data['rolling_mean'] - 2 * ticker_data['adjclose'].rolling(window=window).std()
                ticker_data['signal'] = 0  # 0 means no signal
                ticker_data['signal'][ticker_data['adjclose'] > ticker_data['upper_band']] = 1  # -1 means sell/short
                ticker_data['signal'][ticker_data['adjclose'] < ticker_data['lower_band']] = -1  # 1 means buy/long
                current = ticker_data.iloc[-1]
                signal = current["signal"]
                if signal == 1:
                    cash += -current["adjclose"]
                    print(current["date"],current["adjclose"],"buy",cash)
                elif signal == -1:
                    cash += current["adjclose"]
                    print(current["date"],current["adjclose"],"sell",cash)
                else:
                    print(current["date"],"hold",cash)
                sleep(60*time_between)
    except Exception as e:
        print(str(e))
        continue