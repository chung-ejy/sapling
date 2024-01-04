from backtest_functions.backtest_functions import BacktestFunctions as bf
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view

@csrf_exempt
@api_view(['POST'])
def backtestView(request):
    try:
        if request.method == "POST":
            query = json.loads(request.body)
            complete = bf.backtest(query)
        else:
            complete = {"portfolio":[],"trades":[],"recommendations":[]}
    except Exception as e:
        complete = {"portfolio":[],"trades":[],"recommendations":[]}
        print(str(e))
    return JsonResponse(complete,safe=False)