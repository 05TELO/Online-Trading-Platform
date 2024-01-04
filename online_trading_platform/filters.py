from django_filters import rest_framework as filters

from .models import Merchant


class MerchantFilter(filters.FilterSet):
    country = filters.CharFilter(field_name="contacts__country")
    product_id = filters.NumberFilter(field_name="products__id")

    class Meta:
        model = Merchant
        fields = ["country", "product_id"]
