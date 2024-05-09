from django.urls import path
from contact.views.contact_view import *

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/list/', ContactListView.as_view(), name='contact-list'),
    
    
    path('contact-list-ajax/',ContactDataTablesAjaxPagination.as_view(), name='contact-list-ajax'), 
]