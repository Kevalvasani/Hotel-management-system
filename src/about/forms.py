from django import forms
from .models import *

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = (
            "site_name",
            "description",
            "image",
        )
        widgets = {
            "site_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Site name"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
            "image": forms.FileInput(
                attrs={"class": "form-control", "placeholder": "Image"}
            ),
        }