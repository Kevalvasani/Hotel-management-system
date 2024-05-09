from django import forms
from .models import *

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = (
            'email',
            'phone',
        )
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Phone Number'}),
            }
        
    
    def clean_phone(self):
        phone=self.cleaned_data.get('phone')
        if phone and len(phone)!=10:
            raise forms.ValidationError("Please valid phone number")
        return phone
                

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guest Name', "required": "required"}),
        }

    def clean_name(self):
        phone=self.cleaned_data.get('name')
        if not phone:
            print(222222222222222)
            raise forms.ValidationError("Please enter your name")
        return phone