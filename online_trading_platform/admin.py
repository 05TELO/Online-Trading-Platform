from django.contrib import admin

from . import models


@admin.register(models.Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "contacts",
        "supplier",
        "debt_to_supplier",
        "created_at",
        "type",
    )
    list_filter = ("contacts__city",)  # Фильтр по названию города

    actions = ["clear_supplier_debt"]

    def clear_supplier_debt(self, request, queryset):
        for obj in queryset:
            obj.debt_to_supplier = 0
            obj.save()

    clear_supplier_debt.short_description = "Clear supplier debt"


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "country", "city", "street", "house_number")


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model")


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "salary", "merchant")
