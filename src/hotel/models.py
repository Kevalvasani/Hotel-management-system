from core.models import BaseModel
from django.db import models
from users.models import User
from booking.models import Booking
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum,F
from django.utils import timezone
from datetime import datetime


class Hotel(BaseModel):
    
    manager = models.ForeignKey(User,null=True, on_delete=models.CASCADE,related_name='hotels')
    name = models.CharField(_("Name"), max_length=255)
    owner_name = models.CharField(_("Owner name"),null=True,max_length=255)
    services = models.TextField(_("Servises"),null=True,)
    description = models.TextField(_("Description"), null=True)
    address = models.CharField(_("Address"),max_length=255)
    city= models.CharField(_("City"),max_length=255)
    ratting = models.IntegerField(_("Ratting"),null=True) 
    
    def __str__(self):
        return self.name
    
    def get_available_rooms(self, checkin_date, checkout_date):
        checkin_date = timezone.make_aware(datetime.combine(checkin_date, datetime.min.time()))
        checkout_date = timezone.make_aware(datetime.combine(checkout_date, datetime.min.time()))
        
        # Calculate total booked rooms across all room categories for the given hotel
        total_booked_rooms = Booking.objects.filter(
            hotel=self,
            checkin_date__lt=checkout_date, checkout_date__gt=checkin_date
        ).aggregate(total_booked_rooms=Sum(F('room')))['total_booked_rooms'] or 0
        print("=====",total_booked_rooms)
        # Subtract total booked rooms from the total rooms across all categories for the hotel
        total_rooms_across_categories = RoomCategory.objects.filter(hotel=self).aggregate(total_rooms=Sum('rooms'))['total_rooms'] or 0
        print("....................",total_rooms_across_categories)
        print(total_rooms_across_categories - total_booked_rooms)
        return total_rooms_across_categories - total_booked_rooms
    

    def get_services_list(self):
        return self.services.split(',')
      

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="hotel_image/")

class RoomCategory(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="roomcategories")
    catogory_name= models.CharField(_("Category Name"), max_length=255,null=True)
    rooms = models.IntegerField(_("Rooms"),null=True)
    person = models.CharField(_("Person"),null=True,max_length=255)
    price = models.FloatField(_("Price"),null=True)
    
    def __str__(self):
        return self.catogory_name 

class RoomCategoryImage(models.Model):
    
    roomcategory = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name='room_category')
    image = models.ImageField(upload_to="room_category_images/")   
    
class Rattings(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rattings")
    rattings = models.IntegerField(_("Rattings"))