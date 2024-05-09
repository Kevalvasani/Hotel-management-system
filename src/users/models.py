from django.db import models
from django.contrib.auth.models import AbstractUser,Permission
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
# Create your models here.

class User(BaseModel,AbstractUser):
    hotelmanager = "1"
    customer = "2"
    superadmin = "3"
    
    USER_TYPE_CHOICES = (
        (hotelmanager, "Hotel Manager"),
        (customer, "Customer"),
        (superadmin, "Superadmin")
    )
    email = models.CharField(max_length=255,unique=True)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, default=customer, null=True,blank=None, max_length=15)
    phone_number = models.CharField(max_length=255,unique=True)
    
    
