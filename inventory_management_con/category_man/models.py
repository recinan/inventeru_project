from django.db import models
from django.contrib.auth.models import User
from warehouse_man.models import Warehouse
from django.utils.text import slugify
import uuid

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    warehouse = models.ForeignKey('warehouse_man.Warehouse', on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ('user','warehouse','slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
            while Category.objects.filter(user=self.user, warehouse=self.warehouse,slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name
