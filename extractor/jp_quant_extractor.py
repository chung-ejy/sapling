import requests as r
import json
from dotenv import load_dotenv
load_dotenv()
import os


class JPQuantExtractor(object):

    @classmethod
    def refresh_token(self):
        data={"mailaddress":os.getenv("JPQUANTMAIL"), "password":os.getenv("JPQUANTPW")}
        r_post = r.post("https://api.jquants.com/v1/token/auth_user", data=json.dumps(data))
        return r_post.json()
    
    @classmethod
    def id_token(self,refresh_token):
        r_post = r.post(f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={refresh_token}")
        return r_post.json()

    @classmethod
    def prices(self,refresh_token,ticker,start,end):
        headers = {"Authorization": f"Bearer {refresh_token}"}
        response = r.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={ticker}&start={start}&end={end}", headers=headers)
        return response.json()