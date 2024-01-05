from django.http.response import JsonResponse
from parameter.aparameter import AParameter
from strategy.strategy import Strategy
from database.adatabase import ADatabase

def parameterView(request):
    try:
        if request.method == "GET":
            complete = AParameter().__dict__
        else:
            complete = {}
    except Exception as e:
        complete = {}
        print(str(e))
    return JsonResponse(complete,safe=False)

def healthView(request):
    try:
        if request.method == "GET":
            complete = {"status":"live"}
        else:
            complete = {}
    except Exception as e:
        complete = {}
        print(str(e))
    return JsonResponse(complete,safe=False)

def strategyView(request):
    try:
        if request.method == "GET":
            complete = [x for x in Strategy._value2member_map_.keys()]
        else:
            complete = []
    except Exception as e:
        complete = []
        print(str(e))
    return JsonResponse(complete,safe=False)

def strategyDescriptionsView(request):
    try:
        if request.method == "GET":
            strategies = [x for x in Strategy._value2member_map_.keys()]
            complete = {}
            for strategy in strategies:
                with open(f'./strategy/{strategy.lower()}.py', 'r') as file:
                    strategy_code = file.read()
                complete[strategy] = strategy_code
            with open(f'./parameter/aparameter.py', 'r') as file:
                    strategy_code = file.read()
            complete["parameter"] = strategy_code
        else:
            complete = {}
    except Exception as e:
        complete = []
        print(str(e))
    return JsonResponse(complete,safe=False)

def tickersView(request):
    try:
        if request.method == "GET":
            db = ADatabase("market")
            db.cloud_connect()
            complete = list(db.retrieve("sp100")["ticker"].values)
            db.disconnect()
        else:
            complete = []
    except Exception as e:
        complete = []
        print(str(e))
    return JsonResponse(complete,safe=False)