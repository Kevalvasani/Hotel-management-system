from django.views.generic import CreateView,TemplateView,DetailView,UpdateView,DeleteView
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.db.models import Q, Avg,Count
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic import View
from django_datatables_too.mixins import DataTableMixin
from django.template.loader import render_to_string
from datetime import datetime,timedelta,date
import math
from weasyprint import HTML
from django.urls import reverse
# Models        
from about.models import About
from hotel.models import *
from booking.models import *

# Permissions and Forms
from hotel.permissions import *
from hotel.forms import *

def get_city():
    data = Hotel.objects.all()
    city_list = list(set(i.city for i in data)) 
    return city_list
def set_session_data(request):
    if "person" not in request.session:
        request.session["person"] = 1

    if "city" not in request.session:
        request.session["city"] = "Pune"

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    if "checkin" not in request.session:
        request.session["checkin"] = today.strftime("%Y-%m-%d")

    if "checkout" not in request.session:
        request.session["checkout"] = tomorrow.strftime("%Y-%m-%d")

class DashboardView(ListView):
    template_name = "dashboard.html"
    model = Hotel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_session_data(self.request)
        self.request.session["person"] = 1
        self.request.session["city"] = "Pune"
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        self.request.session["checkin"] = today.strftime("%Y-%m-%d")
        self.request.session["checkout"] = tomorrow.strftime("%Y-%m-%d")
        
        data = Hotel.objects.all()
        hotels=[]
        for hotel in data:
            hotels.append({'hotel':hotel,'average_price':RoomCategory.objects.filter(hotel=hotel).aggregate(Avg("price"))["price__avg"]})
        context['citylist'] = get_city()
        context["about"] = About.objects.all()
        context["hotels"] = hotels[:6]
        context["high_ratings"] = data.order_by('-ratting')[:3]
        context["person"] = self.request.session["person"]
        context["city"] = self.request.session["city"]
        context["checkout"] = self.request.session["checkout"]
        context["checkin"] = self.request.session["checkin"]
        
        return context

class AllHotelView(ListView):

    model = Hotel
    template_name = "all_hotels.html"
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_session_data(self.request)
        data = Hotel.objects.all()
        context["about"] = About.objects.all()
        hotels=[]
        for hotel in data:
            hotels.append({'hotel':hotel,'average_price':RoomCategory.objects.filter(hotel=hotel).aggregate(Avg("price"))["price__avg"]})
        context["all_hotels"] = hotels
        
        person = self.request.session["person"]
        if person is None:
            context["person"] = ""
        else:
            context["person"] = person
        context["city"] = self.request.session["city"]
        context["checkout"] = self.request.session["checkout"]
        context["checkin"] = self.request.session["checkin"]
        context['citylist'] = get_city()
        return context
 
class HotelDetail(DetailView):
    model = Hotel
    template_name = "hotel_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_session_data(self.request)
        hotel = Hotel.objects.filter(pk=self.kwargs['pk']).first()
        context["hotel"] = hotel
        context["about"] = About.objects.all()
        context["rattings"] = Rattings.objects.filter(hotel=hotel).count()
        person = self.request.session["person"]
        if person is None:
            persons = ""
        else:
            persons=person
        context["person"] = persons
        context["city"] = self.request.session["city"]
        checkout_date = self.request.session["checkout"]
        checkin_date = self.request.session["checkin"]
        context["checkout"] = checkout_date
        context["checkin"] = checkin_date

        # Calculate and pass available rooms for each room category
        room_categories = RoomCategory.objects.filter(hotel=hotel)
        available_rooms = []
        for room_category in room_categories:
            total_booked_rooms = Booking.objects.filter(
                hotel=hotel,
                room_category=room_category,
                checkin_date__lt=checkout_date,
                checkout_date__gt=checkin_date
            ).aggregate(Sum('room'))['room__sum'] or 0

            available_rooms.append({
                "category": room_category,
                "available_rooms": room_category.rooms - total_booked_rooms,
                "rooms" : math.ceil(int(persons) / int(room_category.person))
            })
        context['citylist'] = get_city()
        context["available_rooms"] = available_rooms
        return context

    
class AddRattingsView(LoginRequiredMixin, CreateView):
    model=Rattings
    template_name = "rate_feedback.html"
    form_class = Add_RatingForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.hotel = Hotel.objects.get(pk=self.kwargs["hotel_id"])
        messages.success(self.request, "Ratting Done Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Not Save",form.errors)
        return super().form_invalid(form)


    def get_success_url(self, **kwargs):
        return reverse_lazy('hotel_detail', kwargs = {'pk': self.kwargs['hotel_id']})


class HotelSearchView(View):
    template_name = "search_results.html"

    def get(self, request, *args, **kwargs):
        city = self.request.GET.get("city")
        checkin = self.request.GET.get("checkin")
        checkout = self.request.GET.get("checkout")
        person = self.request.GET.get("person")
        request.session["person"] = person
        request.session["city"] = city
        context = {}

        if city and checkin and checkout and person:
            result = Hotel.objects.prefetch_related('images').filter(city__icontains=city)
            persons = int(person)

            if persons <= 0:
                context["errorrooms"] = "Please enter valid input"
                return render(request, self.template_name, context)

            checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
            checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()
            request.session["checkin"] = checkin
            request.session["checkout"] = checkout
            days = (checkout_date - checkin_date).days
            context['days'] = days
            if checkout_date <= checkin_date:
                context["datevalidation"] = (
                    "checkout date should be greater than checkin date."
                )
                return render(request, self.template_name, context)

            available_hotels = []
            data = Hotel.objects.all()
            
            for hotel in result:
                available_rooms = hotel.get_available_rooms(checkin_date, checkout_date)
                rooms= math.ceil( persons / 2)
                context['rooms']=rooms
                if available_rooms >= rooms:
                    available_hotels.append({'hotel':hotel,'average_price':RoomCategory.objects.filter(hotel=hotel).aggregate(Avg("price"))["price__avg"],'rattings':Rattings.objects.filter(hotel=hotel).count()})
            print(available_hotels)    
            context["result"] = available_hotels
            context["about"] = About.objects.all()
        else:
            context["error"] = "Please enter all fields."
            context["result"] = Hotel.objects.all()
            context["about"] = About.objects.all()
            person = self.request.session["person"]
            if person is None:
                context["person"] = ""

            else:
                context["person"] = person
            context["city"] = self.request.session["city"]
            context["checkout"] = self.request.session["checkout"]
            context["checkin"] = self.request.session["checkin"]
            context['citylist'] = get_city()
        return render(request, self.template_name, context)

class ProfileView(LoginRequiredMixin, ListView):
    model = User
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(id=self.request.user.id)
        
        context['bookings'] = Booking.objects.prefetch_related("guests").filter(user=self.request.user)
        context["about"] = About.objects.all()
        
        return context

class PersonalDataView(LoginRequiredMixin, View):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(username=request.user.username).first()
        if user:
            data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'User not found'}, status=404)

class BookingView(LoginRequiredMixin, View):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        bookings = Booking.objects.prefetch_related("guests").filter(user=request.user)
        bookings_data = []
        for booking in bookings:
            guest_name=[guest.name for guest in booking.guests.all()]
            booking_data = {
                'booking_id': booking.id,
                'hotel': booking.hotel.name,
                'guest_name': guest_name,
                'room_category': booking.room_category.catogory_name,
                'room': booking.room,
                'person':booking.person,                
                'checkin_date':booking.checkin_date,
                'checkout_date':booking.checkout_date,
                'amount': booking.amount,
            }
            bookings_data.append(booking_data)
        print(bookings)
        return JsonResponse({'bookings': bookings_data})
    
class DownloadBookingView(View):
    """
    View for downloading tickets.
    """

    def get(self, request, pk):
        """
        Get download ticket.
        """
        user = request.user
        booking = Booking.objects.get(user=user, id=pk)

        context = {
            'booking': booking,
        }
        
        # Render the download_booking template to HTML
        download_details = render_to_string('download_booking.html', context)

        # Create a PDF file using WeasyPrint
        pdf_file = HTML(string=download_details).write_pdf()

        # Create a response with the PDF file
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={booking.hotel.name}_online_hotel_booking.pdf'

        return response


"""
    Hotel Manager Views    
"""


class AddHotelView(IsHotelManager, CreateView):

    model = Hotel
    template_name = "back/add_hotel.html"
    form_class = Add_HotelForm
    success_url = reverse_lazy("show_hotel")

    def form_valid(self, form):
        form.instance.manager = self.request.user
        hotel = form.save()  # Save the hotel instance

        # Save multiple images for the hotel
        images = self.request.FILES.getlist('images')
        for image in images:
            HotelImage.objects.create(hotel=hotel, image=image)
        messages.success(self.request, "Hotel Added Successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        return super().form_invalid(form)


class AddHotelRoomCategoryView(IsHotelManager, CreateView):

    model = RoomCategory
    template_name = "back/add_room_category.html"
    form_class = Add_Room_CategoryForm
    # success_url = reverse_lazy("list_room_category")
  
    def get_success_url(self):
        hotel_id = self.object.hotel.id if self.object.hotel else None
        return reverse_lazy("list_room_category",kwargs={'pk':hotel_id})
    
    def form_valid(self, form):        
        pk = self.kwargs['pk']

        form.instance.manager = self.request.user
        form.instance.hotel = Hotel.objects.get(id=pk)    


        room_category = form.save(commit=False)

        room_category.save() 

        images = self.request.FILES.getlist('images')

        for image in images:
 
            RoomCategoryImage.objects.create(roomcategory=room_category, image=image)
        messages.success(self.request, "Room Category Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return super().form_invalid(form)  
    
class ShowRoomCategory(ListView):
    model = RoomCategory
    template_name = "back/roomcategory.html"
    context_object_name = "room_categories"

    def get_queryset(self):
        hotel_id = self.kwargs['pk']
        return RoomCategory.objects.filter(hotel__id=hotel_id) 


class ManagerShowHotelView(IsHotelManager, TemplateView):
    template_name = "back/show_hotel.html"
    model = Hotel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hotel = Hotel.objects.filter(manager=self.request.user)
        context["hotel"] = hotel
        return context


class EditHotelView(IsHotelManager, UpdateView):
    model = Hotel
    form_class = Edit_HotelForm
    template_name = "back/update_hotel.html"
    # success_url = reverse_lazy("show_hotel")
    context_object_name = "hotel"

    def get_success_url(self):
        hotel_id = self.object.hotel.id if self.object.hotel else None
        return reverse_lazy("list_room_category",kwargs={'pk':hotel_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = HotelImageForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        image_form = HotelImageForm(self.request.POST, self.request.FILES, instance=self.object.images.first())
        
        if form.is_valid() and image_form.is_valid():
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)

    def form_valid(self, form, image_form):
        response = super().form_valid(form)
        image_form.instance.hotel = self.object
        image_form.save()
        messages.success(self.request, "Hotel Update Successfully")
        return response

    def form_invalid(self, form, image_form):
        return self.render_to_response(
            self.get_context_data(form=form, image_form=image_form)
        )


class EditRoomCategoryView(UpdateView):
    model = RoomCategory
    form_class = Edit_RoomCategory_Form
    template_name = "admin/update_room_category.html"
    # success_url = reverse_lazy("room_category_list")
    context_object_name = "roomcategory"

    def get_success_url(self):
        hotel_id = self.object.hotel.id if self.object.hotel else None
        return reverse_lazy("room_category_list",kwargs={'pk':hotel_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = Edit_RoomCategoryImageForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        image_form = Edit_RoomCategoryImageForm(self.request.POST, self.request.FILES, instance=self.object.room_category.first())
        
        if form.is_valid() and image_form.is_valid():
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)

    def form_valid(self, form, image_form):
        response = super().form_valid(form)
        image_form.instance.hotel = self.object
        image_form.save()
        messages.success(self.request, "Room Category Update Successfully")
        return response

    def form_invalid(self, form, image_form):
        return self.render_to_response(
            self.get_context_data(form=form, image_form=image_form)
        )    


class DeleteHotelView(IsHotelManager, DeleteView):

    model = Hotel
    success_url = reverse_lazy("show_hotel")
    template_name = "back/show_hotel.html"

    def post(self, *args, **kwargs):
        id = self.request.POST.get("id", None)
        hotel = Hotel.objects.filter(id=id).first()
        hotel.delete()
        messages.success(self.request, "Hotel Deleted Successfully")
        return JsonResponse({"success": True})


class DeleteRoomCategory(DeleteView):

    model = RoomCategory
    success_url = reverse_lazy("show_hotel")
    template_name = "back/roomcategory.html"

    def post(self, *args, **kwargs):
        id = self.request.POST.get("pk", None)
        print(id)
        roomcategory = RoomCategory.objects.filter(id=id).first()
        print(roomcategory)
        roomcategory.delete()
        messages.success(self.request, f"Room Category Deleted Successfully")
        return JsonResponse({"success": True})

class HotelBookingShowView(IsHotelManager, ListView):
    model = Booking

    template_name = "back/show_booking.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        hotel = Hotel.objects.filter(manager=self.request.user)
        bookings = Booking.objects.filter(hotel__in=hotel).order_by("-booking_date")

        return context


"""
    SuperAdmin Views 
"""


class ShowHotelsToAdminView(IsSuperAdmin, ListView):
    model = Hotel
    template_name = "admin/show_all_hotel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hotel"] = Hotel.objects.all()
        context['today_date'] = date.today()
        
        return context


class ShowAllHotelManagerToAdminView(IsSuperAdmin, ListView):
    model = User
    template_name = "admin/show_hotel_manager.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hotel_manager"] = User.objects.filter(user_type=User.hotelmanager)
        return context


class DeleteHotelManagerView(IsSuperAdmin, DeleteView):
    model = User
    success_url = reverse_lazy("show_all_hotel_manager_to_admin")
    template_name = "admin/show_hotel_manager.html"

    def post(self, *args, **kwargs):
        id = self.request.POST.get("id", None)
        user = User.objects.filter(id=id).first()
        user.delete()
        messages.success(self.request, "Hotel Manager Deleted Successfully")
        return JsonResponse(self.get_success_url())


class EditHotelManagerView(IsSuperAdmin, UpdateView):
    model = User
    form_class = Edit_User_by_AdminForm
    template_name = "admin/update_hotel_manager.html"
    success_url = reverse_lazy("show_all_hotel_manager_to_admin")
    context_object_name = "user"

    def form_valid(self, form):
        messages.success(self.request, "Hotel Manager Details Updated Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class ShowAllRatting(IsSuperAdmin, ListView):
    model = Rattings
    template_name = "admin/rattings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rattings"] = Rattings.objects.all()
        return context
    
class ShowAllCustomerToAdminView(IsSuperAdmin, ListView):
    model = User
    template_name = "admin/show_customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer"] = User.objects.filter(user_type=User.customer)
        return context


class AddHotelByAdminView(IsSuperAdmin, CreateView):

    model = Hotel
    template_name = "admin/add_hotel_admin.html"
    form_class = Add_Hotel_By_AdminForm
    success_url = reverse_lazy("add_hotel_by_admin")
    
    def form_valid(self, form):
        hotel = form.save()  
        images = self.request.FILES.getlist('images')
        for image in images:
            HotelImage.objects.create(hotel=hotel, image=image)
        messages.success(self.request, "Hotel Added Successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        return super().form_invalid(form)


class HotelEditView(IsSuperAdmin, UpdateView):
    model = Hotel
    form_class = EditHotelForm
    template_name = "admin/update_hotel.html"
    success_url = reverse_lazy("show_hotel_to_admin")
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = HotelImageForm(instance=self.object)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        image_form = HotelImageForm(self.request.POST, self.request.FILES, instance=self.object.images.first())
        
        if form.is_valid() and image_form.is_valid():
            
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)
    
    def form_valid(self, form, image_form):
        response = super().form_valid(form)
        image_form.instance.hotel = self.object
        image_form.save()
        messages.success(self.request, "Hotel Updated Successfully")
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)


class HotelDeleteView(IsSuperAdmin, View):
    def post(self, request, *args, **kwargs):
        id = self.request.POST.get("id", None)
        Hotel.objects.filter(id=id).delete()
        messages.success(self.request, "Hotel Deleted Successfully")
        return JsonResponse({"msg": "hotel deleted"})


class AddHotelRoomCategoryByAdminView(IsSuperAdmin, CreateView):

    model = RoomCategory
    template_name = "admin/add_room_category.html"
    form_class = Add_Room_Category_By_AdminForm
    success_url = reverse_lazy("show_hotel_to_admin")

    def form_valid(self, form):        
        pk = self.kwargs['pk']
        form.instance.manager = self.request.user
        form.instance.hotel = Hotel.objects.get(id=pk)    

        room_category = form.save(commit=False)
        room_category.save() 
        images = self.request.FILES.getlist('images')
        for image in images:
            RoomCategoryImage.objects.create(roomcategory=room_category, image=image)
        messages.success(self.request, "Hotel Room Category Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class ShowRoomCategoryToAdmin(IsSuperAdmin,ListView):
    model = RoomCategory
    template_name = "admin/roomcategory.html"
    context_object_name = "room_categories"

    def get_queryset(self):
        hotel_id = self.kwargs['pk']
        return RoomCategory.objects.filter(hotel__id=hotel_id) 


class EditRoomCategoryView( UpdateView):
    model = RoomCategory
    form_class = Edit_RoomCategory_Form
    template_name = "admin/update_room_category.html"
    # success_url = reverse_lazy("room_category_list")
    context_object_name = "roomcategory"

    def get_success_url(self):
        hotel_id = self.object.hotel.id if self.object.hotel else None
        return reverse_lazy("room_category_list",kwargs={'pk':hotel_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = Edit_RoomCategoryImageForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        image_form = Edit_RoomCategoryImageForm(self.request.POST, self.request.FILES, instance=self.object.room_category.first())
        
        if form.is_valid() and image_form.is_valid():
            messages.success(self.request, "Hotel Room Category Updated Successfully")
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)

    def form_valid(self, form, image_form):
        response = super().form_valid(form)
        image_form.instance.hotel = self.object
        image_form.save()
        return response

    def form_invalid(self, form, image_form):
        return self.render_to_response(
            self.get_context_data(form=form, image_form=image_form)
        )    

    
""" 
    DataTables 
"""


class HotelDataTablesAjaxPagination(DataTableMixin, View):
    model = Hotel
    queryset = Hotel.objects.prefetch_related('roomcategories').all()
   
    
    def _get_actions(self, obj):
        #     """Get action buttons w/links."""
        from django.urls import reverse

        edit_url = reverse("edit_hotel_admin", kwargs={"pk": obj.id})
        delete_url = reverse("delete_hotel_admin")
        return f'<a href="{edit_url}" data-id="{obj.id}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-pencil"></i></a> <button data-title="{obj}" data-id="{obj.id}" title="Delete" data-url="{delete_url}" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash"></i></button>'

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        if self.search:
            return qs.filter(
                Q(manager__first_name__icontains=self.search)
                | Q(manager__last_name__icontains=self.search)
                | Q(name__icontains=self.search)
                | Q(owner_name__icontains=self.search)
                | Q(services__icontains=self.search)
                | Q(description__icontains=self.search)
                | Q(address__icontains=self.search)
                | Q(city__icontains=self.search)
            )
        return qs

    def _get_hotel_image(self, obj):
        if obj.images.exists():
            return f'<img src="{obj.images.first().image.url}" style="display: inline-block; width: 50px; height: 50px;"  alt="avatar" class="img-circle">'
        else:
            return 'No Image'
        
    def _get_available_rooms(self,hotel,date):
        # total_rooms = hotel.roomcategories.aggregate(total_rooms=Count('rooms'))['total_rooms']
        total_rooms = RoomCategory.objects.filter(hotel=hotel).aggregate(total_rooms=Sum('rooms'))['total_rooms'] or 0
        booked_rooms = Booking.objects.filter(room_category__hotel=hotel,checkin_date__gte=date).count()
        print(total_rooms,booked_rooms)
        return total_rooms-booked_rooms
    
    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        if self.request.GET.get("datepicker"):
            print("=====>if")
            date = self.request.GET.get("datepicker")
            print("=====>if",date)
        else: 
            date = datetime.now().date()
            print("=====>else",date)
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "image": self._get_hotel_image(o),
                    "manager": o.manager.first_name + " " + o.manager.last_name,
                    "name": o.name,
                    "owner_name": o.owner_name,
                    "services": o.services,
                    "description": o.description,
                    "address": o.address,
                    "city": o.city,
                    "available_room": self._get_available_rooms(o,date),
                    "categories": f'<a href="{reverse("add_hotel_room_category_by_admin", kwargs={"pk": o.id})}" title="Add Room Category" class="btn btn-primary btn-xs"><i class="fa fa-plus-square"></i></a> <a href="{reverse("room_category_list", kwargs={"pk": o.id})}" title="List Room Category" class="btn btn-primary btn-xs"><i class="fa fa-th-list"></i></a>',
                    "action": self._get_actions(o),
                }

            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)

class BookingDataTablesAjaxPagination(DataTableMixin, View):
    model = Booking

    def get_queryset(self):
        queryset = Booking.objects.prefetch_related('guests').all()
        fromdate = self.request.GET.get("fromdate")
        todate = self.request.GET.get("todate")

        if fromdate:
            queryset = Booking.objects.filter(checkin_date=fromdate)

        if fromdate and todate:
            queryset = Booking.objects.filter(
                checkin_date__gte=fromdate, checkout_date__lte=todate
            )
        return queryset

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(hotel__name__icontains=self.search)
                | Q(user__first_name__icontains=self.search)
                | Q(user__last_name__icontains=self.search)
                | Q(email__icontains=self.search)
                | Q(phone__icontains=self.search)
                | Q(room_category__catogory_name__icontains=self.search)
                | Q(room__icontains=self.search)
                | Q(checkin_date__icontains=self.search)
                | Q(checkout_date__icontains=self.search)
                | Q(booking_date__icontains=self.search)
                | Q(amount__icontains=self.search)
                | Q(status__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "hotel": o.hotel.name,
                    "user": o.user.first_name,
                    "email": o.email,
                    "phone": o.phone,
                    "room_category": o.room_category.catogory_name,
                    "room": o.room,
                    "person": o.person,
                    "guests": [{
                        "name": guest.name,
                        }
                        for guest in o.guests.all()
                    ],
                    "checkin_date": o.checkin_date,
                    "checkout_date": o.checkout_date,
                    "booking_date": o.booking_date,
                    "amount": o.amount,
                    "status": o.status,
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)


class HotelManagerDataTablesAjaxPagination(DataTableMixin, View):
    model = User

    def _get_actions(self, obj):
        #     """Get action buttons w/links."""

        edit_url = reverse_lazy("edit_hotel_manager", kwargs={"pk": obj.id})
        delete_url = reverse_lazy("delete_hotel_manager", kwargs={"pk": obj.id})
        return f'<a href="{edit_url}" data-id="{obj.id}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-pencil"></i></a> <button data-title="{obj}" data-id="{obj.id}" title="Delete" data-url="{delete_url}" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash"></i></button>'

    def get_queryset(self):
        """return queryset."""
        qs = User.objects.filter(user_type=User.hotelmanager)
        return qs

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(first_name__icontains=self.search)
                | Q(last_name__icontains=self.search)
                | Q(email__icontains=self.search)
                | Q(username__icontains=self.search)
                | Q(phone_number__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "first_name": o.get_full_name().title(),
                    "username": o.username,
                    "email": o.email,
                    "phone_number": o.phone_number,
                    "action": self._get_actions(o),
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)


class CustomerDataTablesAjaxPagination(DataTableMixin, View):
    model = User

    def _get_actions(self, obj):
        """Get action buttons w/links."""
        edit_url = reverse_lazy("edit_hotel_manager", kwargs={"pk": obj.id})
        delete_url = reverse_lazy("delete_hotel_manager", kwargs={"pk": obj.id})
        return f'<a href="{edit_url}" data-id="{obj.id}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-pencil"></i></a> <button data-title="{obj}" data-id="{obj.id}" title="Delete" data-url="{delete_url}" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash"></i></button>'

    def get_queryset(self):
        """return queryset."""
        qs = User.objects.filter(user_type=User.customer)
        return qs

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(first_name__icontains=self.search)
                | Q(last_name__icontains=self.search)
                | Q(email__icontains=self.search)
                | Q(username__icontains=self.search)
                | Q(phone_number__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "first_name": o.first_name + " " + o.last_name,
                    "username": o.username,
                    "email": o.email,
                    "phone_number": o.phone_number,
                    "action": self._get_actions(o),
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)
    
class RoomCategoryDataTablesAjaxPagination(DataTableMixin, View):
    model = RoomCategory

    def get_queryset(self):
        hotel_id = self.kwargs['pk']
        queryset = RoomCategory.objects.filter(hotel=hotel_id)
        return queryset
    
    def _get_actions(self, obj):
        """Get action buttons w/links."""

        edit_url = reverse_lazy("edit_roomcategory_admin", kwargs={"pk": obj.id})
        delete_url = reverse_lazy("delete_room_category", kwargs={"pk": obj.id})
        return f'<a href="{edit_url}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-pencil"></i></a> <button data-title="{obj}" data-id="{obj.id}" title="Delete" data-url="{delete_url}" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash"></i></button>'


    def filter_queryset(self, qs):#delete_room_category
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(catogory_name__icontains=self.search)
                | Q(rooms__icontains=self.search)
                | Q(person__icontains=self.search)
                | Q(price__icontains=self.search)               
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id, 
                    "catogory_name": o.catogory_name,
                    "rooms": o.rooms,
                    "person": o.person,
                    "price": o.price,
                    "action": self._get_actions(o),
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)




# DataTables Hotel Manager Side
class HotelDitailDataTablesAjaxPagination(DataTableMixin, View):
    model = Hotel

    def get_queryset(self):
        queryset = Hotel.objects.prefetch_related('roomcategories').filter(manager=self.request.user)
        return queryset

    def _get_actions(self, obj):
        from django.urls import reverse

        edit_url = reverse("edit_hotel", kwargs={"pk": obj.id})
        delete_url = reverse("delete_hotel", kwargs={"pk": obj.id})
        return f'<a href="{edit_url}" data-id="{obj.id}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-pencil"></i></a> <button data-title="{obj}" data-id="{obj.id}" title="Delete" data-url="{delete_url}" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash"></i></button>'

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(manager__first_name__icontains=self.search)
                | Q(manager__last_name__icontains=self.search)
                | Q(name__icontains=self.search)
                | Q(owner_name__icontains=self.search)
                | Q(services__icontains=self.search)
                | Q(description__icontains=self.search)
                | Q(address__icontains=self.search)
                | Q(city__icontains=self.search)
                
            )
        return qs

    def _get_hotel_image(self, obj):
        if obj.images.exists():
            return f'<img src="{obj.images.first().image.url}" style="display: inline-block; width: 50px; height: 50px;"  alt="avatar" class="img-circle">'
        else:
            return 'No Image'
    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "manager": o.manager.first_name + " " + o.manager.last_name,
                    "name": o.name,
                    "owner_name": o.owner_name,
                    "description": o.description,
                    "services": o.services,
                    "address": o.address,
                    "city": o.city,
                    "image": self._get_hotel_image(o),
                    "categories": f'<a href="{reverse("add_hotel_room_category", kwargs={"pk": o.id})}" title="Add Room Category" class="btn btn-primary btn-xs"><i class="fa fa-plus"></i></a> <a href="{reverse("list_room_category", kwargs={"pk": o.id})}" title="List Room Category" class="btn btn-primary btn-xs"><i class="fa fa-list" ></i></a>',
                    "action": self._get_actions(o),
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)


class BookingHotelManagerDataTablesAjaxPagination(DataTableMixin, View):
    model = Booking

    def get_queryset(self):
        hotel = Hotel.objects.filter(manager=self.request.user)
        queryset = queryset = Booking.objects.prefetch_related('guests').filter(hotel__in=hotel).order_by("-booking_date")
        fromdate = self.request.GET.get("fromdate")
        todate = self.request.GET.get("todate")

        if fromdate:
            queryset = Booking.objects.filter(checkin_date=fromdate)

        if fromdate and todate:
            queryset = Booking.objects.filter(
                checkin_date__gte=fromdate, checkout_date__lte=todate
            )
        return queryset

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(hotel__name__icontains=self.search)
                | Q(user__first_name__icontains=self.search)
                | Q(user__last_name__icontains=self.search)
                | Q(first_name__icontains=self.search)
                | Q(last_name__icontains=self.search)
                | Q(email__icontains=self.search)
                | Q(phone__icontains=self.search)
                | Q(room_category__catogory_name__icontains=self.search)
                | Q(room__icontains=self.search)
                | Q(checkin_date__icontains=self.search)
                | Q(checkout_date__icontains=self.search)
                | Q(booking_date__icontains=self.search)
                | Q(amount__icontains=self.search)
                | Q(status__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "hotel": o.hotel.name,
                    "user": o.user.first_name,
                    "email": o.email,
                    "phone": o.phone,
                    "room_category": o.room_category.catogory_name,
                    "room": o.room,
                    "person": o.person,
                    "guests": [{
                        "name": guest.name,
                        }
                        for guest in o.guests.all()
                    ],
                    "checkin_date": o.checkin_date,
                    "checkout_date": o.checkout_date,
                    "booking_date": o.booking_date,
                    "amount": o.amount,
                    "status": o.status,
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)


class RattingDataTablesAjaxPagination(DataTableMixin, View):
    model = Rattings

    def get_queryset(self):
        queryset = Rattings.objects.all()
        return queryset

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(user__first_name__icontains=self.search)
                | Q(user__last_name__icontains=self.search)
                | Q(hotel__name__icontains=self.search)
                | Q(rattings__icontains=self.search)

            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "user": o.user.first_name + " " + o.user.last_name,
                    "hotel": o.hotel.name,
                    "rattings": o.rattings
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)