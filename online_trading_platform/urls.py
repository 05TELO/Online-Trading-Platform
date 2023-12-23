from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import ContactViewSet
from .views import EmployeeViewSet
from .views import HealthcheckView
from .views import MerchantAboveAverageDebt
from .views import MerchantViewSet
from .views import ProductViewSet

router = routers.DefaultRouter()
router.register(r"merchants", MerchantViewSet, basename="merchant")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"contacts", ContactViewSet, basename="contact")
router.register(r"employees", EmployeeViewSet, basename="employee")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("merchants/above_average_debt/", MerchantAboveAverageDebt.as_view()),
    path("healthcheck/", HealthcheckView.as_view()),
    path("", include(router.urls)),
]
