from django.urls import reverse
from django.views.generic import View
from django.http import JsonResponse
from contact.models import *
from contact.forms import *
from django.views.generic.list import ListView
from hotel.permissions import *
from django.urls import reverse_lazy
from django_datatables_too.mixins import DataTableMixin
from django.views.generic import View
from django.db.models import Q


class ContactView(View):
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Message sent successfully'
            return JsonResponse({'msg': msg})
        else:
            return JsonResponse({'error': 'Invalid form data'})

class ContactListView(IsSuperAdmin,ListView):

    model = Contact
    template_name = "admin/contact.html"
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["contact"] = Contact.objects.all()
        print(context["contact"])
        return context


class ContactDataTablesAjaxPagination(DataTableMixin, View):
    model = Contact

    def get_queryset(self):
        queryset = Contact.objects.all()
        
        return queryset
    def _get_actions(self, obj):

        reply_url = "#"
        return f'<a href="{reply_url}" data-id="{obj.id}" title="Reply" class="btn btn-primary btn-xs"><i class="fa fa-reply" style="font-size:48px;color:red"></i></a>'

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(name__icontains=self.search)
                | Q(phone_number__icontains=self.search)
                | Q(email__icontains=self.search)
                | Q(message__icontains=self.search)
            )
        return qs
    
    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "name": o.name,
                    "phone_number": o.phone_number,
                    "email":o.email,
                    "message":o.message,
                    "action":self._get_actions(o)                  
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        print(context_data)
        return JsonResponse(context_data)
