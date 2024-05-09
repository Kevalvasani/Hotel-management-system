from typing import Any
from django.shortcuts import render, redirect
from users.forms import *
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
import random
from booking.tasks import success_message


class CustomerRegistrationView(CreateView):
    model = User
    template_name = "customer_registration.html"
    form_class = CustomerRegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]
        search = email.rfind("@")
        e_u = User.objects.values_list("username", flat=True)
        username = email[:search]
        while username in e_u:
            username += str(random.randint(0, 9999))
        user.username = username
        user.set_password(password)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class HotelManagerRegistrationView(CreateView):
    model = User
    template_name = "hotel_manager_registration.html"
    form_class = HotelManagerRegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        phone_no = form.cleaned_data["phone_number"]
        password = form.cleaned_data["password"]
        print(phone_no)
        email = form.cleaned_data["email"]
        search = email.find("@")
        e_u = User.objects.values_list("username", flat=True)
        username = email[:search]
        while username in e_u:
            username += str(random.randint(0, 9999))
        user.username = username
        user.phone_number = phone_no
        user.set_password(password)
        user.user_type = User.hotelmanager
        user.is_active = True
        user.is_staff = True
        user = super().form_valid(form)
        msg = f"User created successfully done. \n Username : is '{username}' \n Password: '{password}'"
        success_message(email, msg)
        return user

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class MyLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.user_type == "2":
            return reverse_lazy("dashboard")
        elif self.request.user.user_type == "3":
            return reverse_lazy("adminportel")
        return reverse_lazy("managerportel")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class MyLogoutView(LogoutView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard")


class ManagerPortelView(TemplateView):
    template_name = "back/master.html"


class AdminPortelView(TemplateView):
    template_name = "admin/master.html"
