from random import randint

from celery import shared_task
from django.db.models import F

from .models import Merchant


@shared_task
def increase_debt() -> None:
    merchants = list(Merchant.objects.all())
    for merchant in merchants:
        increase_amount = randint(5, 500)
        merchant.debt_to_supplier = F("debt_to_supplier") + increase_amount
    Merchant.objects.bulk_update(merchants, ["debt_to_supplier"])


@shared_task
def reduce_debt() -> None:
    merchants = list(Merchant.objects.all())
    for merchant in merchants:
        amount = randint(100, 10000)
        merchant.debt_to_supplier = F("debt_to_supplier") - amount
    Merchant.objects.bulk_update(merchants, ["debt_to_supplier"])


@shared_task
def clear_supplier_debt_async(ids: list) -> None:
    merchants = list(Merchant.objects.filter(id__in=ids))
    for merchant in merchants:
        merchant.debt_to_supplier = 0
    Merchant.objects.bulk_update(merchants, ["debt_to_supplier"])
