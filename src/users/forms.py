from django import forms
from users.models import User

class CustomerRegisterForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Re-enter Password'}))
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',            
            'phone_number',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'password'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'phone_number'})
            }
    def clean_phone_number(self):
        phone=self.cleaned_data.get('phone_number')
        if phone and len(phone)!=10:
            raise forms.ValidationError("Please valid phone number")
        return phone
    
    def clean_password_confirm(self):
        password=self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passowrd do not match.")
        return password_confirm

            
class HotelManagerRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            # 'username',
            'email',
            'password',            
            'phone_number',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}),
            # 'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'username'}),
            'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'password'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'phone_number'}),
            }
    
    def clean_phone_number(self):
        phone=self.cleaned_data.get('phone_number')
        print(phone)
        if phone and len(phone)!=10:
            print(phone)
            raise forms.ValidationError("Please enter valid phone number")
        return phone

            
            
