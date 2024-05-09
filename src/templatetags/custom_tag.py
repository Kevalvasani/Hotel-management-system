from django import template 
register = template.Library()

@register.filter(name="is_hotel_manager")
def is_hotel_manager(user):
    return user.is_authenticated and user.user_type == '1'
