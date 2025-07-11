# Generated by Django 5.1.4 on 2025-07-04 19:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0004_alter_country_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="educationstage",
            name="countries",
            field=models.ManyToManyField(
                related_name="education_stages", to="course.country"
            ),
        ),
        migrations.AlterField(
            model_name="educationstage",
            name="country",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="education_stages_country",
                to="course.country",
            ),
        ),
    ]
