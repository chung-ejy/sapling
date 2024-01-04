from backtest_functions.backtest_functions import BacktestFunctions as bf
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from database.adatabase import ADatabase
import pandas as pd
from datetime import datetime
import json

@csrf_exempt
def backtestView(request):
    try:
        if request.method == "GET":
            query = {key: value for key, value in request.GET.items()}
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