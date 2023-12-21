from django.urls import path, include

urlpatterns = [
    path('backtest/',include('backtest.urls')),
    path('info/',include('info.urls')),
]
