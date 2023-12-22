from django.urls import include
from django.urls import path

urlpatterns = [
    path("api/", include("online_trading_platform.urls")),
]
