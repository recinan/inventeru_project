from django.db import models
from django.contrib.auth.models import User
from warehouse_man.models import Warehouse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    warehouse = models.ForeignKey('warehouse_man.Warehouse', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.category_name
