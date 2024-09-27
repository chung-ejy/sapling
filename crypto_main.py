from extractor.alp_client_extractor import ALPClientExtractor
from trading_client.alpaca_client import AlpacaClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
from time import sleep
import warnings
warnings.simplefilter(action="ignore")


## parameters

client = AlpacaClient()
window = 300
gain_window = 60
req = 0.005
floor = -0.005
metric = "rolling_return"
ascending = False
timeframe = 300
extractor = ALPClientExtractor(os.getenv("APCAKEY"), os.getenv("APCASECRET"))
tickers = ["AAVE", "AVAX", "BAT", "BTC", "CRV", "DOGE", "DOT", "ETH", "GRT", "LINK", "LTC", "MKR", "SHIB", "SUSHI", "UNI", "XTZ", "YFI"]
tickers = [x + "/USD" for x in tickers]

while True:
    try:
        prices = []
        start = datetime.now() - timedelta(days=5)
        end = datetime.now()

        # Loop through each ticker to fetch prices and calculate metrics
        for ticker in tickers:
            response = extractor.crypto_interval(ticker, start)
            price = pd.DataFrame(response["bars"][ticker]).rename(columns={"c": "adjclose", "t": "date"})[["date", "adjclose"]]
            
            # Convert date and sort
            price["date"] = pd.to_datetime(price["date"])
            price = price.sort_values("date")
            
            # Calculate metrics
            price["rolling_return"] = ((price["adjclose"].rolling(window).mean() - price["adjclose"]) / price["adjclose"])
            price["bollinger"] = ((price["adjclose"].rolling(window).mean() - price["adjclose"].rolling(window).std() - price["adjclose"]) / price["adjclose"])
            price["return"] = price["adjclose"].pct_change(gain_window)
            price["avg_return"] = price["return"].pct_change(gain_window).rolling(window).mean()
            price["coev"] = (price["adjclose"].rolling(window).mean() / price["adjclose"].rolling(window).std())
            price["ticker"] = ticker
            prices.append(price)

        # Combine all prices into a single DataFrame
        sim = pd.concat(prices).sort_values("date").dropna()
        recommendations = sim.groupby("ticker").last().reset_index()
        recommendations["currency"] = [x.split("/")[0] for x in recommendations["ticker"]]
        recommendation = recommendations.sort_values(metric,ascending=ascending).iloc[0]
        positions = client.positions()
        if positions.index.size > 0:
            position = positions.to_dict("records")[0]
            position_data = recommendations[recommendations["currency"]==position["symbol"][:-3]].iloc[0]
            pnl = (float(position_data["adjclose"])-float(position["avg_entry_price"])) / float(position["avg_entry_price"])
            # print(client.account()["portfolio_value"],pnl)
            if True:
                client.close()
                sleep(60)
                account = client.account()
                cash = float(account["cash"])
                client.crypto_buy(recommendation["ticker"],cash)
        else:
            account = client.account()
            cash = float(account["cash"])
            client.crypto_buy(recommendation["ticker"],cash)
    except Exception as e:
        print(str(e))
    sleep(timeframe)