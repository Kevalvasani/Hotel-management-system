from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class Users(admin.ModelAdmin):
    list_display=['id','first_name','last_name','username','email',"phone_number","user_type"]