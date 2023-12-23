from django.db import models


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
        limit_choices_to={"type__lt": 4},
    )
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.PositiveIntegerField(choices=TYPE_CHOICES)

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


class Employee(models.Model):
    merchant = models.ForeignKey(
        Merchant, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField()
    position = models.CharField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name
