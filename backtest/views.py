from backtest_functions.backtest_functions import BacktestFunctions as bf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http.response import JsonResponse
from database.adatabase import ADatabase
import pandas as pd
from datetime import datetime
import json

@ensure_csrf_cookie
def backtestView(request):
    try:
        if request.method == "POST":
            query = json.loads(request.body)
            complete = bf.backtest(query)
            query_df = pd.DataFrame([query])
            query_df["date"] = datetime.now()
            sapling = ADatabase("sapling")
            sapling.cloud_connect()
            sapling.store("queries",query_df)
            sapling.disconnect()
        else:
            complete = {"portfolio":[],"trades":[],"recommendations":[]}
    except Exception as e:
        complete = {"portfolio":[],"trades":[],"recommendations":[]}
        print(str(e))
    return JsonResponse(complete,safe=False)

@ensure_csrf_cookie
def marketView(request):
    try:
        if request.method == "GET":
            complete = bf.market()
        else:
            complete = []
    except Exception as e:
        complete = []
        print(str(e))
    return JsonResponse(complete,safe=False)