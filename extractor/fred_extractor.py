import pandas as pd
import requests as r
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("FREDKEY")

class FREDExtractor(object):

    @classmethod
    def cpi(self):
        headers = {
            "accept":"application/json"
        }
        params = {
            "api_key":token,
            "series_id":"CPIAUCSL",
            "file_type":"json"
        }
        url = "https://api.stlouisfed.org/fred/series/observations"
        requestBody = r.get(url,params=params,headers=headers)
        return pd.DataFrame(requestBody.json()["observations"])

    @classmethod
    def oil(self):
        headers = {
            "accept":"application/json"
        }
        params = {
            "api_key":token,
            "series_id":"DCOILWTICO",
            "file_type":"json"
        }
        url = "https://api.stlouisfed.org/fred/series/observations"
        requestBody = r.get(url,params=params,headers=headers)
        return pd.DataFrame(requestBody.json()["observations"])

    @classmethod
    def exports(self):
        headers = {
            "accept":"application/json"
        }
        params = {
            "api_key":token,
            "series_id":"NETEXP",
            "file_type":"json"
        }
        url = "https://api.stlouisfed.org/fred/series/observations"
        requestBody = r.get(url,params=params,headers=headers)
        return pd.DataFrame(requestBody.json()["observations"])

    @classmethod
    def gdp(self):
        headers = {
            "accept":"application/json"
        }
        params = {
            "api_key":token,
            "series_id":"GDP",
            "file_type":"json"
        }
        url = "https://api.stlouisfed.org/fred/series/observations"
        requestBody = r.get(url,params=params,headers=headers)
        return pd.DataFrame(requestBody.json()["observations"])
    
    
    @classmethod
    def unrate(self):
        headers = {
            "accept":"application/json"
        }
        params = {
            "api_key":token,
            "series_id":"UNRATE",
            "file_type":"json"
        }
        url = "https://api.stlouisfed.org/fred/series/observations"
        requestBody = r.get(url,params=params,headers=headers)
        return pd.DataFrame(requestBody.json()["observations"])
    
    @classmethod
    def sp500(self):
        headers = {
            "accept":"application/json"
        }
        params = {
            "api_key":token,
            "series_id":"SP500",
            "file_type":"json"
        }
        url = "https://api.stlouisfed.org/fred/series/observations"
        requestBody = r.get(url,params=params,headers=headers)
        return pd.DataFrame(requestBody.json()["observations"])

    @classmethod
    def treasury_yields(self):
        headers = {
            "accept":"application/json"
        }
        params = {
            "api_key":token,
            "series_id":"DGS1",
            "file_type":"json"
        }
        url = "https://api.stlouisfed.org/fred/series/observations"
        requestBody = r.get(url,params=params,headers=headers)
        return pd.DataFrame(requestBody.json()["observations"])