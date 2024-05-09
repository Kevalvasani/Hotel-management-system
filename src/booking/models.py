from django.db import models
from users.models import User
from core.models import *

# Create your models here.
class Booking(models.Model):
    
    hotel = models.ForeignKey("hotel.Hotel", related_name="booking", on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, related_name="booking", on_delete=models.CASCADE)
    email = models.CharField(default=None, max_length=64)
    phone = models.CharField(default=None, max_length=64)
    room_category = models.ForeignKey("hotel.RoomCategory", null=True, blank=True,on_delete=models.CASCADE)
    room = models.IntegerField(default=1)
    person = models.IntegerField(default=1)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    booking_date = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=64, default=None, null=False)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.email
    
class Guest(BaseModel):
    booking = models.ForeignKey(Booking, related_name="guests", on_delete=models.CASCADE,null=True)
    name = models.CharField(default=None, max_length=64,null=True)
    
    def __str__(self):
        return self.name