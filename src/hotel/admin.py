from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Hotel)
class Hotel(admin.ModelAdmin):
    list_display=['id','name','address','city']

@admin.register(HotelImage)
class HotelImage(admin.ModelAdmin):
    list_display=['hotel','image']

@admin.register(RoomCategory)
class RoomCategory(admin.ModelAdmin):
    list_display=['id','hotel','catogory_name','person','price']


@admin.register(RoomCategoryImage)
class RoomCategoryImage(admin.ModelAdmin):
    list_display=['roomcategory','image']

@admin.register(Rattings)
class Rattings(admin.ModelAdmin):
    list_display=['user','hotel','rattings']