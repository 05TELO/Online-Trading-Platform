from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.urls import path

urlpatterns = [
    path("api/", include("online_trading_platform.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
