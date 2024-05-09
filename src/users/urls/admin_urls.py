from django.contrib import admin
from django.urls import path,include
from users.views.views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("customer_register/", CustomerRegistrationView.as_view(), name="customer_register"),
    path("accounts/login/", MyLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("managerportel/", ManagerPortelView.as_view(), name="managerportel"),
    path("hotel_manager_register/", HotelManagerRegistrationView.as_view(), name="hotel_manager_register"),
    path("adminportel/", AdminPortelView.as_view(), name="adminportel"),
]