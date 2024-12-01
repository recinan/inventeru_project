from django.db import models
from django.contrib.auth.models import User
from warehouse_man.models import Warehouse
from category_man.models import Category
# Create your models here.

class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    category = models.ForeignKey('category_man.Category', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('warehouse_man.Warehouse', on_delete=models.SET_NULL, blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

