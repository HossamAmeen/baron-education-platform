from django.db import models
from django_extensions.db.models import TimeStampedModel


class PasswordReset(TimeStampedModel):
    email = models.EmailField()
    token = models.CharField(max_length=100)
