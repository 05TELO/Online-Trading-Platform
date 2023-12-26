from typing import Any

from django.contrib.auth import authenticate
from django.db.models import Avg
from django.db.models.query import QuerySet
from rest_framework import authentication
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response

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

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        country = self.request.query_params.get("country")
        product_id = self.request.query_params.get("product_id")

        #        queryset = queryset.filter(employee=self.request.user)

        if country:
            queryset = queryset.filter(contacts__country=country)

        if product_id:
            queryset = queryset.filter(products__id=product_id)

        return queryset

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
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, format: None = None) -> Response:
        average_debt = Merchant.objects.aggregate(Avg("debt_to_supplier"))[
            "debt_to_supplier__avg"
        ]
        merchants_above_average_debt = Merchant.objects.filter(
            debt_to_supplier__gt=average_debt
        )
        if merchants_above_average_debt:
            serializer = MerchantSerializer(
                merchants_above_average_debt, many=True
            )
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
