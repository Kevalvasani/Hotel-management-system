from django.urls import path
from about.views.about_views import *

urlpatterns=[
    path("about/", AboutView.as_view(), name='about'),
    path("about/update/<int:pk>/", UpdateAboutView.as_view(), name='update-about'),
    path("about/delete/<int:pk>/", DeleteAboutView.as_view(), name='delete-about'),
    
    path('site-list-ajax/', SiteDataTablesAjaxPagination.as_view(), name='site-list-ajax'), 
]