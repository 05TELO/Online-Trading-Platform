from typing import Any

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from .managers import EmployeeManager


class Merchant(models.Model):
    TYPE_CHOICES = (
        (0, "Factory"),
        (1, "Distributor"),
        (2, "Dealer Center"),
        (3, "Large Retail Network"),
        (4, "Individual Entrepreneur"),
    )

    name = models.CharField()
    contacts = models.OneToOneField(
        "Contact", on_delete=models.SET_NULL, null=True, blank=True
    )
    products = models.ManyToManyField("Product")
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    type = models.PositiveIntegerField(choices=TYPE_CHOICES)

    def clean(self) -> None:
        if self.supplier and self.supplier.type >= self.type:
            raise ValidationError("Supplier must have a lower 'type' value.")

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    email = models.EmailField()
    country = models.CharField()
    city = models.CharField()
    street = models.CharField()
    house_number = models.CharField()

    def __str__(self) -> str:
        return self.email


class Product(models.Model):
    name = models.CharField()
    model = models.CharField()
    release_date = models.DateField()

    def __str__(self) -> str:
        return self.name


class Employee(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True)
    merchant = models.ForeignKey(
        Merchant, on_delete=models.SET_NULL, null=True, blank=True
    )
    position = models.CharField(null=True, blank=True)
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS: list = []

    def __str__(self) -> str:
        return self.username
