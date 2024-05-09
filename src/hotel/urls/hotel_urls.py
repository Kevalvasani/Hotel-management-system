from django.urls import path
from hotel.views.hotels_view import *


urlpatterns = [
       path("", DashboardView.as_view(), name="dashboard"),
       path("allhotels/", AllHotelView.as_view(), name="allhotels"),
       path("hotel/<int:pk>/", HotelDetail.as_view(), name="hotel_detail"),
       path("add/ratting/<int:hotel_id>/", AddRattingsView.as_view(), name="add_ratting"),       
       path("hotel/search/", HotelSearchView.as_view(), name="hotel_search"),
       
       #   Hotel Mangers urls
      
       path("add/hotel/", AddHotelView.as_view(), name="add_hotel"),
       path("hotel/", ManagerShowHotelView.as_view(), name="show_hotel"),
       path("add/hotel/room/category/<int:pk>/", AddHotelRoomCategoryView.as_view(), name="add_hotel_room_category"),
       path("hotel/roomcategories/<int:pk>/",ShowRoomCategory.as_view(), name="list_room_category"),
       path("hotel/roomcategories/<int:pk>/delete", DeleteRoomCategory.as_view(), name="delete_room_category"),
       path("hotel/<int:pk>/edit/", EditHotelView.as_view(), name="edit_hotel"),
       path("hotel/<int:pk>/delete", DeleteHotelView.as_view(), name="delete_hotel"),
       path("download/booking/<int:pk>", DownloadBookingView.as_view(), name="download_booking"),
       
       #   Super Admin urls
       path("profile", ProfileView.as_view(), name="profile"),
       path("personal-data/", PersonalDataView.as_view(), name="personal_data_view"),
       path("booking/", BookingView.as_view(), name="booking_view"),
       path('hotel/manager/',ShowAllHotelManagerToAdminView.as_view(), name="show_all_hotel_manager_to_admin"),
       path('add/hotel/admin/', AddHotelByAdminView.as_view(), name="add_hotel_by_admin"),
       path('hotel/edit/<int:pk>/manager', EditHotelManagerView.as_view(), name="edit_hotel_manager"),
       path('hotel/delete/<int:pk>/manager',DeleteHotelManagerView.as_view(),name='delete_hotel_manager'),
       path('customer/list/',ShowAllCustomerToAdminView.as_view(), name="show_all_customer_to_admin"),
       path('hotel/list/',ShowHotelsToAdminView.as_view(), name="show_hotel_to_admin"),
       path("add/roomcategory/<int:pk>/", AddHotelRoomCategoryByAdminView.as_view(), name="add_hotel_room_category_by_admin"),
       path("hotel/edit/<int:pk>/",HotelEditView.as_view(), name="edit_hotel_admin"),
       path("hotel/roomcategory/edit/<int:pk>/",EditRoomCategoryView.as_view(), name="edit_roomcategory_admin"),
       path("hotel/delete/",HotelDeleteView.as_view(), name="delete_hotel_admin"),
       path('ratting/',ShowAllRatting.as_view(), name="show_all_ratting"), 
       path("hotel/<int:pk>/roomcategories/",ShowRoomCategoryToAdmin.as_view(), name="room_category_list"),
       
       
       
       # DataTables views
       path('hotel-list-ajax',HotelDataTablesAjaxPagination.as_view(), name='hotel-list-ajax'),           
       path('booking-list-ajax',BookingDataTablesAjaxPagination.as_view(), name='booking-list-ajax'),
       path('hotelmanager-list-ajax',HotelManagerDataTablesAjaxPagination.as_view(), name='hotelmanager-list-ajax'),
       path('customer-list-ajax',CustomerDataTablesAjaxPagination.as_view(), name='customer-list-ajax'),
       path('ratting-list-ajax',RattingDataTablesAjaxPagination.as_view(), name='ratting-list-ajax'),
       path('roomcategory-list-ajax/<int:pk>',RoomCategoryDataTablesAjaxPagination.as_view(), name='roomcategory-list-ajax'),
       
       # DataTables Admin Side         
       path('hotel-detail-list-ajax',HotelDitailDataTablesAjaxPagination.as_view(), name='hotel-detail-list-ajax'),
       path('booking-detail-list-ajax',BookingHotelManagerDataTablesAjaxPagination.as_view(), name='booking-detail-list-ajax'),
]      


