from . import views
from django.urls import path

urlpatterns = [
    path("parameter",views.parameterView,name="parameter"),
    path("strategy",views.strategyView,name="strategy"),
    path("strategy/descriptions",views.strategyDescriptionsView,name="strategy_description"),
]