from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from parameter.aparameter import AParameter
from strategy.strategy import Strategy
@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
def strategyDescriptionsView(request):
    try:
        if request.method == "GET":
            strategies = [x.lower() for x in Strategy._value2member_map_.keys()]
            complete = {}
            for strategy in strategies:
                with open(f'./strategy/{strategy}.py', 'r') as file:
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