from typing import Any

from django.contrib.auth import authenticate
from django.db.models import Avg, Window, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import authentication
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response

from online_trading_platform.filters import MerchantFilter

from . import permissions as cust_perm
from .models import Merchant
from .models import Product
from .serializers import MerchantSerializer
from .serializers import ProductSerializer


class HealthcheckView(generics.GenericAPIView):
    def get(self, request: Request) -> Response:
        return Response({"message": "healthy"})


class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        cust_perm.IsActiveEmployee,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MerchantFilter

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data["debt_to_supplier"] = request.data.get(
            "debt_to_supplier", 0
        )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Merchant deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class MerchantAboveAverageDebt(generics.ListAPIView):
    serializer_class = MerchantSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Merchant.objects.annotate(
            avg_debt=Window(expression=Avg('debt_to_supplier'))
        ).filter(debt_to_supplier__gt=F('avg_debt'))

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"message": "No merchants with above average debt"})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        cust_perm.IsActiveEmployee,
    ]

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class LoginView(generics.GenericAPIView):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response(
                {"error": "Wrong Credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )
