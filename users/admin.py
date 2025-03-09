from django.contrib import admin
from django.contrib.auth.models import Group

# flake8: noqa
# Register your models here.
admin.site.unregister(Group)