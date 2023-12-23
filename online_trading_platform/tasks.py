from random import randint

from celery import shared_task

from .models import Merchant


@shared_task
def increase_debt() -> None:
    merchants = Merchant.objects.all()
    for merchant in merchants:
        increase_amount = randint(5, 500)
        merchant.debt_to_supplier += increase_amount
        merchant.save()


@shared_task
def reduce_debt() -> None:
    merchants = Merchant.objects.all()
    for merchant in merchants:
        amount = randint(100, 10000)
        merchant.debt_to_supplier -= amount
        merchant.save()


@shared_task
def clear_supplier_debt_async(ids):
    queryset = Merchant.objects.filter(id__in=ids)
    for obj in queryset:
        obj.debt_to_supplier = 0
        obj.save()
