from django.db import models

# Create your models here.

class Plan(models.Model):
    plan_name = models.CharField(max_length=50)
    warehouse_limit = models.PositiveIntegerField(default=1)
    category_per_warehouse_limit = models.PositiveIntegerField(default=3)
    products_per_category_limit = models.PositiveIntegerField(default=20)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return self.plan_name