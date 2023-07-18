# Generated by Django 4.1.7 on 2023-07-17 10:56

import Solver.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserImages",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "img",
                    models.ImageField(
                        null=True, upload_to=Solver.models.generate_filename
                    ),
                ),
            ],
        ),
    ]