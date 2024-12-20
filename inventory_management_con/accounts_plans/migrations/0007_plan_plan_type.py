# Generated by Django 5.1.2 on 2024-12-19 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts_plans", "0006_remove_plan_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="plan_type",
            field=models.CharField(
                choices=[
                    ("monthly", "Monthly"),
                    ("annual", "Annual"),
                    ("infinite", "Infinite"),
                ],
                default="monthly",
                max_length=15,
            ),
        ),
    ]
