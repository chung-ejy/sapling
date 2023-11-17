import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("FMPKEY")
import requests as r

class FMPExtractor(object):

    @classmethod
    def balance_sheet(self,ticker):
        headers = {
            "accept":"application/json"
        }
        params = {
            "apikey":token,
            "period":"annual"
        }
        url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}"
        requestBody = r.get(url,params=params,headers=headers)
        return pd.DataFrame(requestBody.json())