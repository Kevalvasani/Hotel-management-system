from django.db import models
from users.models import User
from core.models import BaseModel

class Contact(BaseModel):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
    
    