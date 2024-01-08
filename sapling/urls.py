from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Add this line to include the default admin URL
    path('backtest/', include('backtest.urls')),
    path('info/', include('info.urls')),
    path('security_functions/',include('security_functions.urls')),
    path('auth/', include('authentication.urls')),
    path("",include("frontend.urls")),
]
