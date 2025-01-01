from django.db import models
from django.utils.text import slugify
import uuid
from django.conf import settings
from django.utils.timezone import now, make_aware
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
# Create your models here.

class Plan(models.Model):
    PLAN_TYPE_CHOICES = [
        ("monthly","Monthly"),
        ("annual","Annual"),
        ("infinite","Infinite")
    ]
    plan_name = models.CharField(max_length=50)
    plan_description = models.TextField(blank=True, default="---")
    warehouse_limit = models.PositiveIntegerField(default=1)
    category_per_warehouse_limit = models.PositiveIntegerField(default=3)
    products_per_category_limit = models.PositiveIntegerField(default=20)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    is_default = models.BooleanField(default=False)
    plan_type = models.CharField(max_length=15, choices=PLAN_TYPE_CHOICES, default="monthly")

    def __str__(self):
        return self.plan_name
    
class Subscription(models.Model):
    sub_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sub_plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    sub_start_date = models.DateTimeField(default=now)
    sub_end_date = models.DateTimeField(null=True, blank=True)
    sub_is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.sub_plan:
            default_plan = Plan.objects.filter(is_default=True).first()
            if default_plan:
                self.sub_plan = default_plan

        if not self.sub_end_date:
            self.sub_end_date = self.sub_start_date + timedelta(days=30)

        super().save(*args, **kwargs)

    def is_subscription_active(self):
        if self.sub_end_date and now > self.sub_end_date:
            self.is_active = False
            self.save()
        return self.sub_is_active