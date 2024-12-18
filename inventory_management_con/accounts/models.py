from django.contrib.auth.models import AbstractUser
from django.db import models
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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
