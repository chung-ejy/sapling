from trader.live_trader import LiveTrader
from trading_client.alpaca_live_client import AlpacaLiveClient
from strategy.average_return_strategy import AverageReturnStrategy
from parameter.aparameter import AParameter
import pandas as pd
import warnings
from processor.processor import Processor as processor
from database.adatabase import ADatabase
from time import sleep
import  os
from datetime import datetime, timedelta
from extractor.alp_client_extractor import ALPClientExtractor
from dotenv import load_dotenv
from tqdm import tqdm
from arch import arch_model
warnings.simplefilter(action="ignore")
load_dotenv()
db = ADatabase("sapling")
import numpy as np

try:
    sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",attrs={"id":"constituents"})[0].rename(columns={"Symbol":"ticker"})
    tickers = sp500["ticker"]
    trading_client = AlpacaLiveClient()
    strategy = AverageReturnStrategy(AParameter(1))
    prices = processor.column_date_processing(trading_client.bar(tickers))
    if prices.index.size > 0:
        sim = []
        chunks = [tickers[i:i + 25] for i in range(0, len(tickers), 25)]
        for chunk in chunks:
            try:
                ticker_data = ALPClientExtractor(key=os.getenv("APCAKEY"),secret=os.getenv("APCASECRET")).prices_bulk(",".join(chunk),datetime.now() - timedelta(days=150),datetime.now())
                sleep(1)
                for key in ticker_data["bars"].keys():
                    price = pd.DataFrame(ticker_data["bars"][key]).rename(columns={"c":"adjclose","t":"date","l":"adjlow","h":"adjhigh","v":"volume"})[["date","adjclose","adjlow","adjhigh","volume"]]
                    price["ticker"] = key
                    sim.append(price)
            except Exception as e:
                print(str(e))
        sim = pd.concat(sim)
        datas = []
        for ticker in tickers:
            try:
                price = processor.column_date_processing(sim[sim["ticker"]==ticker]).sort_values("date")
                returns = price["adjclose"].pct_change(5).dropna()
    
                # Fit ARMA(1,1) model with GARCH(1,1) errors
                model = arch_model(returns, mean='AR', lags=1, vol='Garch', p=1, q=1)
                garch_fit = model.fit(disp='off')
                
                # Make predictions
                forecasts = garch_fit.forecast(horizon=returns.size)
                mean_forecast = forecasts.mean
                variance_forecast = forecasts.variance.iloc[-1, :]
                forecasts = [0 for i in range(price.index.size - len(mean_forecast.values[0]))]
                forecasts.extend(mean_forecast.values[0])
                price["garch"] = forecasts
                datas.append(price.iloc[-1].dropna())
            except Exception as e:
                print(str(e))
                continue
        stuff = pd.DataFrame(datas)
        sim = strategy.preprocessing(stuff,prices)
        trader = LiveTrader(trading_client=trading_client,strategy=strategy)
        # print(sim.sort_values(strategy.ranker,ascending=strategy.ascending))
        trader.trade(sim)
except Exception as e:
    print(str(e))
