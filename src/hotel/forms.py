from django import forms
from .models import *
from multiupload.fields import MultiFileField


class Add_HotelForm(forms.ModelForm):
    images = MultiFileField(
        min_num=1, max_num=10, max_file_size=1024 * 1024 * 5, required=False
    )

    class Meta:
        model = Hotel
        fields = (
            "name",
            "owner_name",
            "services",
            "description",
            "address",
            "city",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Hotel name"}
            ),
            "owner_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Owner Name"}
            ),
            "services": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Services"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
            "address": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Address"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            
        }


class Add_Room_CategoryForm(forms.ModelForm):
    images = MultiFileField(
        min_num=1, max_num=10, max_file_size=1024 * 1024 * 5, required=False
    )

    class Meta:
        model = RoomCategory
        fields = ("catogory_name", "person", "rooms", "price")

        widgets = {
            
            "catogory_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Category Name"}
            ),
            "rooms": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Total No. Rooms"}
            ),
            "person": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "No. of Persons in 1 Room",
                }
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Price 1 Room/Day"}
            ),
        }


class Add_RatingForm(forms.ModelForm):
    class Meta:
        model = Rattings
        fields = ["rattings"]


class HotelImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ("image",)


class Edit_HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = (
            "name",
            "owner_name",
            "services",
            "description",
            "address",
            "city",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Hotel Name"}
            ),
            "owner_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Owner Name"}
            ),
            "services": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Services"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
            "address": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Address"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            )
        }


class Edit_User_by_AdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Username"}
            ),
            "email": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "phone_number": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Phone number"}
            ),
        }


class Add_Hotel_By_AdminForm(forms.ModelForm):
    images = MultiFileField(
        min_num=1, max_num=10, max_file_size=1024 * 1024 * 5, required=False
    )

    class Meta:
        model = Hotel
        fields = (
            "manager",
            "name",
            "owner_name",
            "services",
            "description",
            "address",
            "city",
        )
        widgets = {
            "manager": forms.Select(
                attrs={"class": "form-control", "placeholder": "Hotel Manager"}
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Hotel Name"}
            ),
            "owner_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Owner Name"}
            ),
            "services": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Servises"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
            "address": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Address"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(Add_Hotel_By_AdminForm, self).__init__(*args, **kwargs)
        manager = User.objects.filter(user_type="1")
        self.fields["manager"].queryset = manager


class Add_Room_Category_By_AdminForm(forms.ModelForm):
    images = MultiFileField(
        min_num=1, max_num=10, max_file_size=1024 * 1024 * 5, required=False
    )

    class Meta:
        model = RoomCategory
        fields = ("catogory_name", "person", "rooms", "price")
        # "hotel",
        widgets = {
            "catogory_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Category Name"}
            ),
            "rooms": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Total Rooms"}
            ),
            "person": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "No. of Persons in 1 Room",
                }
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Price 1 room/day"}
            ),
        }


class EditHotelForm(forms.ModelForm):

    class Meta:
        model = Hotel
        fields = (
            "name",
            "owner_name",
            "services",
            "description",
            "address",
            "city",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Hotel Name"}
            ),
            "owner_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Owner Name"}
            ),
            "services": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Servises"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
            "address": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Address"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
        }

class Edit_RoomCategoryImageForm(forms.ModelForm):
    class Meta:
        model = RoomCategoryImage
        fields = ("image",)

class Edit_RoomCategory_Form(forms.ModelForm):
    class Meta:
        model = RoomCategory
        fields = (
            "catogory_name",
            "rooms",
            "person",
            "price",
        )
        widgets = {
            "catogory_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Room Category Name"}
            ),
            "rooms": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Total Rooms"}
            ),
            "person": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Person"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Price"}
            )
        }
