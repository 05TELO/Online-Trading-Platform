from typing import Optional

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html
from rest_framework.request import Request

from . import forms
from . import models
from .tasks import clear_supplier_debt_async


@admin.register(models.Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "id",
        "contacts",
        "supplier_link",
        "debt_to_supplier",
        "created_at",
        "type",
    )
    list_filter = ("contacts__city",)

    actions = ["clear_supplier_debt"]

    def clear_supplier_debt(
        self, request: Request, queryset: QuerySet
    ) -> None:
        if queryset.count() > 20:
            ids = list(queryset.values_list("id", flat=True))
            clear_supplier_debt_async.delay(ids)
            self.message_user(
                request, "Clear supplier debt task has been scheduled."
            )
        else:
            for obj in queryset:
                obj.debt_to_supplier = 0
                obj.save()
            self.message_user(request, "Supplier debt has been cleared.")

    def supplier_link(self, obj: models.Employee) -> Optional[str]:
        if obj.supplier is not None:
            url = reverse(
                "admin:online_trading_platform_merchant_change",
                args=[obj.supplier.id],
            )
            return format_html(
                '<a href="{}" style="color: blue;">{}</a>', url, obj.supplier
            )
        else:
            return "(No supplier)"

    supplier_link.short_description = "Supplier"  # type: ignore


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "id", "country", "city", "street", "house_number")


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "model")


@admin.register(models.Employee)
class EmployeeAdmin(UserAdmin):
    add_form = forms.EmployeeCreationForm
    form = forms.EmployeeChangeForm
    model = models.Employee
    list_display = (
        "username",
        "id",
        "merchant",
        "position",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "username",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("username", "merchant", "position", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "merchant",
                    "position",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)
