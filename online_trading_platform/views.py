from django.db.models import Avg
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Contact
from .models import Employee
from .models import Merchant
from .models import Product
from .serializers import ContactSerializer
from .serializers import EmployeeSerializer
from .serializers import MerchantSerializer
from .serializers import ProductSerializer


class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.query_params.get("country")
        product_id = self.request.query_params.get("product_id")

        if country:
            queryset = queryset.filter(contacts__country=country)

        if product_id:
            queryset = queryset.filter(products__id=product_id)

        return queryset

    def create(self, request, *args, **kwargs) -> Response:
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

    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Merchant deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class MerchantAboveAverageDebt(generics.ListAPIView):
    def get(self, request: Request, format=None) -> Response:
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

    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Contact deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Employee deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
