from django.db import models
from django.contrib.auth.models import User
from warehouse_man.models import Warehouse
from category_man.models import Category
from django.utils.text import slugify
import uuid
# Create your models here.

class InventoryItem(models.Model):
    item_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    category = models.ForeignKey('category_man.Category', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('warehouse_man.Warehouse', on_delete=models.SET_NULL, blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Inventory Items'
        unique_together = ('user','warehouse','category','slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.item_name)
            while InventoryItem.objects.filter(user=self.user, warehouse=self.warehouse,category=self.category,slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.item_name

