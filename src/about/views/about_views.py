from django.views.generic.list import ListView
from hotel.permissions import *
from about.models import About
from django.views.generic import UpdateView,DeleteView
from about.forms import AboutForm
from django.urls import reverse_lazy
from django_datatables_too.mixins import DataTableMixin
from django.http import JsonResponse
from django.views.generic import View
from django.db.models import Q


 
class AboutView(IsSuperAdmin,ListView):
    model = About
    template_name = "admin/about.html"
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["about"] = About.objects.all()
        print(context["about"])
        return context

    
    
class UpdateAboutView(IsSuperAdmin, UpdateView):
    model = About
    form_class = AboutForm
    template_name = "admin/update_about.html"
    success_url = reverse_lazy("about")
    context_object_name = "about"

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
class DeleteAboutView(IsSuperAdmin, DeleteView):
    model = About
    success_url = reverse_lazy("about")
    template_name = "admin/about.html"

    def post(self, *args, **kwargs):
        id = self.request.POST.get("id", None)
        user = About.objects.filter(id=id).first()
        user.delete()

        return JsonResponse(self.get_success_url())
    
    

class SiteDataTablesAjaxPagination(DataTableMixin, View):
    model = About

    def get_queryset(self):
        queryset = About.objects.all()
        
        return queryset
    def _get_actions(self, obj):
        #     """Get action buttons w/links."""
        from django.urls import reverse

        edit_url = reverse("update-about", kwargs={"pk": obj.id})
        print(edit_url)
        delete_url = reverse("delete-about", kwargs={"pk": obj.id})
        return f'<a href="{edit_url}" data-id="{obj.id}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-pencil"></i></a> <button data-title="{obj}" data-id="{obj.id}" title="Delete" data-url="{delete_url}" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash"></i></button>'

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(site_name__icontains=self.search)
                | Q(description__icontains=self.search)
            )
        return qs
    def _get_hotel_image(self, obj):
        return f'<img src="{obj.image.url}" style="display: inline-block; width: 50px; height: 50px;"  alt="avatar" class="img-circle">'

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "site_name": o.site_name,
                    "description": o.description,
                    "image": self._get_hotel_image(o),
                    "action": self._get_actions(o),
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        print(context_data)
        return JsonResponse(context_data)
