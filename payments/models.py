from django.db import models
from django_extensions.db.models import TimeStampedModel

from users.models import UserAccount


class Transaction(TimeStampedModel):
    class TransactionStatus(models.TextChoices):
        PENDING = 'pending'
        PAID = 'paid'
        FAILED = 'failed'

    gateway_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
