from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name= "Warehouse"

    def __str__(self) -> str:
        return self.warehouse_name