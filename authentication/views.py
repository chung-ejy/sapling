from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import json
from database.adatabase import ADatabase
import pandas as pd 

@require_POST
def signup_view(request):
    ## make sure no repeat users
    user=json.loads(request.body)
    mt = ADatabase("mistletoe")
    mt.cloud_connect()
    mt.store("users",pd.DataFrame([user]))
    mt.disconnect()
    return JsonResponse({'message': 'User created successfully'}, status=201)


## bad boy security problems
@api_view(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body)
        mt = ADatabase("mistletoe")
        mt.cloud_connect()
        user = mt.query("users",data).to_dict("records")[0]
        mt.disconnect() 
        if user is not None:
            return JsonResponse({'message': 'Login successful',"user":user,"token":7}, status=200)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON data'}, status=400)
