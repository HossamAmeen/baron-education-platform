# Generated by Django 5.1.4 on 2025-03-10 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_transaction_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='currency',
            field=models.CharField(default='asd', max_length=3),
            preserve_default=False,
        ),
    ]
