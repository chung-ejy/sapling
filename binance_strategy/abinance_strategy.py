import pandas as pd
from datetime import datetime
class ABinanceStrategy(object):

    def __init__(self,parameter):
        for key in parameter.__dict__.keys():
            self.__setattr__(key,parameter.__dict__[key])

    def load_umf(self,umf):
        self.umf = umf

    def overhead(self):
        columns = ["start","open","high","low","close","volume","end","volume","trades","buy_volume","base_volume","ignore"]
        df = pd.DataFrame(data=self.umf.klines(self.ticker,interval="1m"),columns=columns)
        df["date"] = [datetime.utcfromtimestamp(int(x/1000)) for x in df["start"]]
        df.sort_values("date",inplace=True)
        df["close"] = [float(x) for x in df["close"]]
        df["rolling"] = df["close"].rolling(self.band).mean()
        df["signal"] = df["rolling"] > df["close"]
        df["signal"] = [1 if x == True else -1 for x in df["signal"]]
        return  df.iloc[-1]
        