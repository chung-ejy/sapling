# authentication/views.py
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

@require_POST
def signup_view(request):
    serializer = SignupSerializer(data=request.POST)
    if serializer.is_valid():
        user = serializer.save()
        return JsonResponse({'message': 'User created successfully'}, status=201)
    return JsonResponse({'errors': serializer.errors}, status=400)

@require_POST
def login_view(request):
    serializer = LoginSerializer(data=request.POST)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return JsonResponse({'message': 'Login successful', 'token': access_token}, status=200)
    return JsonResponse({'errors': serializer.errors}, status=400)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
