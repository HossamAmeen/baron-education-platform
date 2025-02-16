# Generated by Django 5.1.4 on 2025-02-04 10:43

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='admin',
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='manager',
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='student',
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='teacher',
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='useraccount',
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='useraccount',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
