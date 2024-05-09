from django.contrib.auth.mixins import *
from users.models import User
from users.urls.admin_urls import *
from django.shortcuts import redirect

class IsSuperAdmin(LoginRequiredMixin):
    def handle_404(self):
        """Handel 404 error."""
        return redirect("login")

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif request.user.user_type != User.superadmin:
            return self.handle_404()
        
        return super().dispatch(request, *args, **kwargs)

class IsHotelManager(LoginRequiredMixin):
    def handle_404(self):
        """Handel 404 error."""
        return redirect("login")

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif request.user.user_type != User.hotelmanager:
            return self.handle_404()
        
        return super().dispatch(request, *args, **kwargs)
