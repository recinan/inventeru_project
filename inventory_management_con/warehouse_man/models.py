from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural= "Warehouses"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.warehouse_name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.warehouse_name