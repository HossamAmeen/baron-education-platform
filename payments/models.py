from django.db import models
from django_extensions.db.models import TimeStampedModel

from shared.constants import CurrencyCHOICES
from users.models import User


class Transaction(TimeStampedModel):
    class TransactionStatus(models.TextChoices):
        PENDING = "pending"
        PAID = "paid"
        FAILED = "failed"

    currency = models.CharField(
        max_length=3, choices=CurrencyCHOICES.choices, default=CurrencyCHOICES.EGP
    )
    gateway_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )
    client_secret = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.amount} {self.currency}"
