from datetime import date

from django.utils import timezone
from rest_framework import serializers

from .models import Contact
from .models import Employee
from .models import Merchant
from .models import Product


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = "__all__"
        read_only_fields = ("debt_to_supplier",)

    def validate_name(self, value: str) -> str:
        if len(value) > 50:
            raise serializers.ValidationError(
                "Merchant name cannot exceed 50 characters."
            )
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate_name(self, value: str) -> str:
        if len(value) > 25:
            raise serializers.ValidationError(
                "Product name cannot exceed 25 characters."
            )
        return value

    def validate_release_date(self, value: date) -> date:
        if value > timezone.now().date():
            raise serializers.ValidationError(
                "Invalid release date; it cannot be in the future."
            )
        return value


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
