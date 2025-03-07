from django.db import models


class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)

