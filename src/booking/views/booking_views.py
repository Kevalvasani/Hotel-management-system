from booking.models import *
from django.views.generic import (
    CreateView,
    DeleteView,
)
from django.forms import formset_factory

from django.urls import reverse_lazy
from booking.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from hotel.urls.hotel_urls import *
from datetime import datetime
from hotel.permissions import *
import math
from booking.tasks import success_message,cancel_booking_message
from django.contrib.messages.views import messages
from django.db import transaction


class HotelBookingView(LoginRequiredMixin, CreateView):

    model = Booking
    template_name = "booking.html"
    form_class = BookingForm
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_pk"] = self.kwargs.get("pk")
        person = self.request.session.get("person")
        city = self.request.session.get("city")
        checkout_date = self.request.session.get("checkout")
        checkin_date = self.request.session.get("checkin")
        checkin = (
            datetime.strptime(checkin_date, "%Y-%m-%d").date() if checkin_date else None
        )
        checkout = (
            datetime.strptime(checkout_date, "%Y-%m-%d").date()
            if checkout_date
            else None
        )

        if person is not None:
            persons = int(person)
        else:
            persons = 0

        context["checkout"] = checkout
        context["city"] = city
        context["checkin"] = checkin

        if checkin and checkout:
            total_days = (checkout - checkin).days
        else:
            total_days = 0

        context["total_days"] = total_days
        hotel_instance = RoomCategory.objects.filter(pk=context["room_pk"])
        for i in hotel_instance:
            if i.rooms >= 0:
                price = i.price
                total_rooms = math.ceil(persons / int(i.person))
            else:
                total_rooms = 0
            context["hotel"] = i
        context["total_rooms"] = total_rooms
        context["person"] = person
        context["total_price"] = context["total_days"] * context["total_rooms"] * price
        context["discount"] = context["total_price"] / 10
        after_discount = context["total_price"] - (context["total_price"] / 10)
        context["after_discount"] = after_discount
        context["about"] = About.objects.all()
        field = 20 if persons >= 20 else persons
        context["guest_form"] = formset_factory(GuestForm, extra=field)

        return context

    def form_valid(self, form):
        checkin = self.get_context_data().get("checkin")
        checkout = self.get_context_data().get("checkout")
        if not (checkin and checkout):
            error = {}
            error["msg"] = "please enter a dates"
            return error

        email = form.cleaned_data["email"]
        days = self.get_context_data().get("total_days")
        room_pk = self.get_context_data().get("room_pk")
        hotel = get_object_or_404(RoomCategory, pk=room_pk)
        total_amount = self.get_context_data().get("after_discount")
        form.instance.email = email
        form.instance.phone = form.cleaned_data["phone"]
        form.instance.checkin_date = checkin
        form.instance.checkout_date = checkout
        form.instance.person = self.request.session["person"]
        form.instance.room = self.get_context_data().get("total_rooms")

        form.instance.amount = total_amount
        form.instance.hotel = hotel.hotel
        form.instance.room_category = hotel
        form.instance.user = self.request.user
        form.instance.status = 1
        guest_formset = self.get_context_data().get("guest_form")(self.request.POST)
        print("111111",guest_formset)
        if guest_formset.is_valid():
            with transaction.atomic():
                data = super().form_valid(form)
                
                if guest_formset:
                    for guest_form in guest_formset:     
                        guest_form.instance.booking = form.instance
                        print("111111",guest_form)
                        guest_form.save()
                data["msg"] = "Booking successfully done"
                success_message.delay(email, data['msg'])
                messages.success(self.request, "Hotel Booking Successfully")
        else:
            data={}
            data['error'] = "Guest Details are Required."
        
        return data
        

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

class AllBookingtoAdminView(IsSuperAdmin, ListView):
    model = Booking
    template_name = "admin/all_booking.html"
    context_object_name = "booking"


class HotelBookingShowView(IsHotelManager, ListView):
    model = Booking
    template_name = "back/show_booking.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        hotel = Hotel.objects.filter(manager=self.request.user)
        bookings = Booking.objects.filter(hotel__in=hotel).order_by("-booking_date")

        context["booking"] = bookings
        return context


class CancelBookingsView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = "profile.html"
    success_url = reverse_lazy("profile")

    def delete(self, request, *args, **kwargs):
        booking = Booking.objects.filter(id=self.pk)
        s = timezone.now() + timedelta(days=2)
        print(booking)
        if booking.checkin >= s:
            cancellation_charges = 0.20 * float(booking.amount)
            refund_amount = float(booking.amount) - cancellation_charges
            messages.success(self.request, "Hotel booking cancel.")
            cancel["msg"] = f"Booking successfully done. \n your refund amount ₹{refund_amount} will be refunded"
            cancel_booking_message.delay(booking.email, cancel['msg'])
            print('email:',booking.email,'msg :',cancel["msg"])
            cancel = super().delete(request, **args, **kwargs)
            return cancel
        else:
            err = {}
            err["dd"] = "not deleted"
            print(err["dd"])
            return err
