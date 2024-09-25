from extractor.alp_client_extractor import ALPClientExtractor
from trading_client.alpaca_client import AlpacaClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
from time import sleep


while True:
    try:
        start = datetime.now() - timedelta(days=2)
        extractor = ALPClientExtractor(os.getenv("APCAKEY"),os.getenv("APCASECRET"))
        tickers = ["AAVE", "AVAX", "BAT", "BCH", "BTC", "CRV", "DOGE", "DOT", "ETH", "GRT", "LINK", "LTC", "MKR", "SHIB", "SUSHI","USDT","USDC", "UNI", "XTZ", "YFI"]
        tickers = [x +"/USD" for x in tickers]
        prices = []
        for ticker in tickers:
            response = extractor.crypto(ticker,start)
            price = pd.DataFrame(response["bars"][ticker]).rename(columns={"c":"adjclose","t":"date"})[["date","adjclose"]]
            price["date"] = pd.to_datetime(price["date"])
            price = price.sort_values("date")
            price["rolling_return"] = ((price["adjclose"].rolling(30).mean() - price["adjclose"]) / price["adjclose"])
            price["return"] = price["adjclose"].pct_change(5)
            price["avg_return"] = price["return"].rolling(30).mean()
            price["coev"] = (price["adjclose"].rolling(30).mean() / price["adjclose"].rolling(30).std())
            price["ticker"]= ticker
            prices.append(price)

        prices = pd.concat(prices).sort_values("date").dropna()
        recommendations = prices[prices["date"]==prices["date"].max()]
        recommendation = recommendations.sort_values("rolling_return",ascending=False).iloc[0]
        client = AlpacaClient()
        account = client.account()
        cash = float(account["cash"])
        client.close()
        sleep(60)
        client.buy(recommendation["ticker"],recommendation["adjclose"],cash)
        sleep(300)
    except Exception as e:
        print(str(e))
        