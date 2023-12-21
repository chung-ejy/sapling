from . import views
from django.urls import path

urlpatterns = [
    path("parameter",views.parameterView,name="parameter"),
    path("strategy",views.strategyView,name="strategy"),
]