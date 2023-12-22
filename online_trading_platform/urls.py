from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import MerchantViewSet, MerchantAboveAverageDebt, ProductViewSet, ContactViewSet, EmployeeViewSet

router = routers.DefaultRouter()
router.register(r'merchants', MerchantViewSet, basename='merchant')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("merchants/above_average_debt/", MerchantAboveAverageDebt.as_view()),
    path("", include(router.urls)),
]
