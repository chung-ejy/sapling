from extractor.alp_client_extractor import ALPClientExtractor
from trading_client.alpaca_client import AlpacaClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
from time import sleep
client = AlpacaClient()
window = 100
extractor = ALPClientExtractor(os.getenv("APCAKEY"),os.getenv("APCASECRET"))
tickers = ["AAVE", "AVAX", "BAT", "BTC", "CRV", "DOGE", "DOT", "ETH", "GRT", "LINK", "MKR", "SHIB", "SUSHI", "UNI", "XTZ", "YFI"]
tickers = [x +"/USD" for x in tickers]

while True:
    try:
        prices = []
        start = datetime.now() - timedelta(hours=12)
        end = datetime.now()
        for ticker in tickers:
            response = extractor.crypto_interval(ticker,start)
            price = pd.DataFrame(response["bars"][ticker]).rename(columns={"c":"adjclose","t":"date"})[["date","adjclose"]]
            price["date"] = pd.to_datetime(price["date"])
            price = price.sort_values("date")
            price["rolling_return"] = ((price["adjclose"].rolling(window).mean() - price["adjclose"]) / price["adjclose"])
            price["bollinger"] = ((price["adjclose"].rolling(window).mean() - price["adjclose"].rolling(window).std() - price["adjclose"]) / price["adjclose"])
            price["return"] = price["adjclose"].pct_change(5)
            price["avg_return"] = price["return"].rolling(window).mean()
            price["coev"] = (price["adjclose"].rolling(window).mean() / price["adjclose"].rolling(window).std())
            price["ticker"]= ticker
            prices.append(price)

        sim = pd.concat(prices).sort_values("date").dropna()
        recommendations = sim[sim["date"]==sim["date"].max()]
        recommendation = recommendations.sort_values("avg_return",ascending=False).iloc[0]
        positions = client.positions()
        if positions.index.size > 0:
            position = positions.to_dict("records")[0]
            pnl = round(float(position["unrealized_pl"]) / float(position["cost_basis"]),5)
            # print(client.account()["portfolio_value"],pnl)
            if pnl >= 0.05 or pnl <= -0.05:
                client.close()
                sleep(60)
                account = client.account()
                cash = float(account["cash"])
                print(client.crypto_buy(recommendation["ticker"],cash))
        else:
            account = client.account()
            cash = float(account["cash"])
            print(client.crypto_buy(recommendation["ticker"],cash))
    except Exception as e:
        print(str(e))
    sleep(60)