# Generated by Django 5.1.4 on 2024-12-09 20:28
# flake8: noqa
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='user_permissions',
        ),
    ]