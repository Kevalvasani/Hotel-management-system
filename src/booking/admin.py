from django.contrib import admin
from booking.models import *
# Register your models here.
@admin.register(Booking)
class Booking(admin.ModelAdmin):
    list_display=['id','user','hotel','room_category','email','phone','person','room','checkin_date','checkout_date','amount','status']
    
@admin.register(Guest)
class Guest(admin.ModelAdmin):
    list_display=['id','booking','name']