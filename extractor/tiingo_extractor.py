import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("TIINGOKEY")
import requests as r

class TiingoExtractor(object):

    @classmethod
    def prices(self,ticker,start,end):
        params = {
            "token":token,
            "startDate":start.strftime("%Y-%m-%d"),
            "endDate":end.strftime("%Y-%m-%d"),
            "format":"json",
            "resampleFreq":"daily"
        }
        url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices/"
        requestBody = r.get(url,params=params)
        return pd.DataFrame(requestBody.json())