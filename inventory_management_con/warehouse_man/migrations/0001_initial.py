# Generated by Django 5.1.2 on 2024-12-18 13:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Warehouse",
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
                ("warehouse_name", models.CharField(max_length=100)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "neighborhood",
                    models.CharField(blank=True, default="", max_length=100),
                ),
                ("street", models.CharField(blank=True, default="", max_length=150)),
                ("district", models.CharField(max_length=100)),
                ("postal_code", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("country", models.CharField(default="Türkiye", max_length=100)),
                ("slug", models.SlugField(blank=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Warehouses",
                "unique_together": {("user", "slug")},
            },
        ),
    ]
