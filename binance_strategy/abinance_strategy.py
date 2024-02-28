import pandas as pd
from datetime import datetime
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from catboost import CatBoostRegressor
import warnings
warnings.simplefilter(action="ignore")
from database.adatabase import ADatabase
import pytz
kst_timezone = pytz.timezone('Asia/Seoul')

class ABinanceStrategy(object):

    def __init__(self,parameter):
        for key in parameter.__dict__.keys():
            self.__setattr__(key,parameter.__dict__[key])

    def load_umf(self,umf):
        self.umf = umf

    def overhead(self):
        columns = ["start","open","high","low","close","volume","end","volume","trades","buy_volume","base_volume","ignore"]
        factors = [str(i) for i in range(10)]
        df = pd.DataFrame(data=self.umf.klines(self.ticker,interval="1m",limit=1000),columns=columns)
        df["date"] = [datetime.utcfromtimestamp(int(x/1000)) for x in df["start"]]
        df.sort_values("date",inplace=True)
        df["close"] = [float(x) for x in df["close"]]
        for i in range(10):
            df[str(i)] = df["close"].shift(i)
        df["y"] = df["close"].shift(-5)
        training = df.iloc[:950].dropna()
        predictions = df.iloc[950:]
        model1 = LinearRegression(fit_intercept=True)
        model1.fit(training[factors],training["y"])
        model2 = CatBoostRegressor(verbose=False)
        model2.fit(training[factors],training["y"])
        model3 = XGBRegressor()
        model3.fit(training[factors],training["y"])
        predictions["prediction1"] =  model1.predict(predictions[factors])
        predictions["prediction2"] =  model2.predict(predictions[factors])
        predictions["prediction3"] =  model3.predict(predictions[factors])
        predictions["prediction"] = (predictions["prediction1"] + predictions["prediction2"] + predictions["prediction3"]) / 3
        df = predictions[["date","close","prediction"]].copy()
        df["signal"] = df["prediction"] > df["close"]
        df["signal"] = [1 if x == True else - 1 for x in df["signal"]]
        
        trades = self.umf.get_account_trades("XRPUSDT")
        trades = pd.DataFrame(trades)
        trades["date"] = [datetime.utcfromtimestamp(float(x) // 1000.0).replace(tzinfo=pytz.utc).astimezone(kst_timezone) for x in trades["time"]]
        trades["realizedPnl"] = [round(float(x),3) for x in trades["realizedPnl"]]
        trades["commission"] = [round(float(x),3) for x in trades["commission"]]
        trades["price"] = [round(float(x),4) for x in trades["price"]]
        trades["w/l"] = ["W" if x > 0.1 else  "L" if x < 0.00 else "N" if x == 0 else "BE" for x in trades["realizedPnl"]]
        trades = trades.groupby(["date","w/l"]).agg({"price":"mean","commission":"sum","realizedPnl":"sum"}).reset_index()
        trades["agg_pnl"] = [round(x,3) for x in trades["realizedPnl"].cumsum()]
        trades["agg_commission"] = [round(x,3) for x in trades["commission"].cumsum()]
        trades["pnl"] = trades["agg_pnl"] - trades["agg_commission"]
        trades["entry_price"] = trades["price"].shift(1)
        trades["price_diff"] = [round(x,2) for x in trades["price"].pct_change() * 100]
        trades["net_profit"] = trades["realizedPnl"] - trades["commission"]
        trades = trades[(trades["w/l"]!="N")]
        trades = trades[["date","price","entry_price","price_diff","w/l","net_profit","realizedPnl","agg_pnl","commission","agg_commission","pnl"]]
        trades["date"] = [str(x) for x in trades["date"]]
        db = ADatabase("sapling")
        db.cloud_connect()
        db.drop("crypto_trades")
        db.store("crypto_trades",trades.sort_values("date",ascending=False).round(3))
        db.disconnect()
        
        return  df.iloc[-1]
        