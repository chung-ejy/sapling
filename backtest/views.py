from backtest_functions.backtest_functions import BacktestFunctions as bf
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def backtestView(request):
    try:
        if request.method == "POST":
            query = json.loads(request.body)
            complete = bf.backtest(query)
        else:
            complete = {}
    except Exception as e:
        complete = {}
        print(str(e))
    return JsonResponse(complete,safe=False)
