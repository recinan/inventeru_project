from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

# Create your models here.
class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural= "Warehouses"
        unique_together = ('user','slug')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.warehouse_name)
            while Warehouse.objects.filter(user=self.user, slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.warehouse_name