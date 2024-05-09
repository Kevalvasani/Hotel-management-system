from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            "name",
            "phone_number",
            "email",
            "message",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Name"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "email": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "email"}
            ),
            "message": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "message"}
            ),
        }