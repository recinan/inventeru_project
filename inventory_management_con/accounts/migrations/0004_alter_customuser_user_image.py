# Generated by Django 5.1.2 on 2024-12-18 09:18

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_customuser_user_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="user_image",
            field=models.ImageField(
                blank=True,
                default="images/user_images/user.png",
                null=True,
                upload_to=accounts.models.CustomUser.image_upload_to,
            ),
        ),
    ]
