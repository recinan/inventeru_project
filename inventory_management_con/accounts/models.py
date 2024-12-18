from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts_plans.models import Plan
import os
# Create your models here.

class CustomUser(AbstractUser):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('images/user_images/',self.username,instance)
        return None
    STATUS = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15,unique=True)
    status = models.CharField(max_length=100,choices=STATUS, default='regular')
    user_image = models.ImageField(null=True,blank=True, upload_to=image_upload_to, default="images/user_images/user.jpg")
    user_plan = models.ForeignKey('accounts_plans.Plan', on_delete=models.SET_NULL, null=True, blank=True)

    def get_warehouse_limit(self):
        if self.user_plan:
            return self.user_plan.warehouse_limit
        else:
             self.user_plan.warehouse_limit = 1
             return self.user_plan.warehouse_limit

    def get_category_per_warehouse_limit(self):
        if self.user_plan:
            return self.user_plan.category_per_warehouse_limit
        else:
            self.user_plan.category_per_warehouse = 3
            return self.user_plan.category_per_warehouse_limit
    def get_products_per_category_limit(self):
        if self.user_plan:
            return self.user_plan.products_per_category_limit
        else:
            self.user_plan.products_per_category = 20
            return self.user_plan.products_per_category_limit

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
