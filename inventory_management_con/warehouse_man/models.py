from django.db import models

# Create your models here.
class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name= "Warehouse"

    def __str__(self) -> str:
        return self.name