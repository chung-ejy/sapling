import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("FREDKEY")
import requests as r

class FREDExtractor(object):

    @classmethod
    def market_yield(self,start,end):
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "api_key":token,
            "observation_start":start.strftime("%Y-%m-%d"),
            "observation_end":end.strftime("%Y-%m-%d"),
            "file_type":"json",
            "series_id":"DGS10"
        }
        requestBody = r.get(url,params=params)
        return pd.DataFrame(requestBody.json()["observations"])
    
    @classmethod
    def sp500(self,start,end):
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "api_key":token,
            "observation_start":start.strftime("%Y-%m-%d"),
            "observation_end":end.strftime("%Y-%m-%d"),
            "file_type":"json",
            "series_id":"SP500"
        }
        requestBody = r.get(url,params=params)
        return pd.DataFrame(requestBody.json()["observations"])