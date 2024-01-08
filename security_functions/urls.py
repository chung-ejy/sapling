from . import views
from django.urls import path

urlpatterns = [
    path("token",views.tokenView,name="token"),
]