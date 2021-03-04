import re

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": "Password"
        }
    ))


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs ={
        "class": "form-control",
        "placeholder": "username"
    }))
    first_name = forms.CharField(label='First name', max_length=20, required=True, widget=forms.TextInput(
        attrs ={
        "class": "form-control",
        "placeholder": "First name"
    }))
    last_name = forms.CharField(label='Last name', max_length=20, required=True, widget=forms.TextInput(
        attrs ={
        "class": "form-control",
        "placeholder": "Last name"
    }))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "placeholder": "email"
        }
    ))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": "password"
        }))
    confirmation_pass = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(   attrs={
            # "class": "form-control",
            "placeholder": "Confirm password"
        }))
    phone = forms.CharField(label='Phone number', required=False, widget=forms.TextInput(
        attrs ={
        # "class": "form-control",
        "placeholder": "xxx-xxx-xxxx"
    }))
    address = forms.CharField(label="Address", required=True, widget=forms.TextInput(
        attrs={
        "class": "form-control",
        "placeholder": "neighborhood/apartment name, number, street",
        "size": '40'
    }))
    city = forms.CharField(label="City", max_length=15, required=True, widget=forms.TextInput(
        attrs ={
        "class": "form-control",
        "placeholder": "city"
    }))
    zip_code = forms.CharField(label="Zip code", max_length=10, required=True, widget=forms.TextInput(
        attrs ={
        "class": "form-control",
        "placeholder": "zipcode"
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        queryset = User.objects.filter(username=username)
        if queryset.exists() and self.instance is None:
            raise forms.ValidationError("Username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        queryset = User.objects.filter(email=email)
        if queryset.exists() and self.instance is None:
            raise forms.ValidationError("Email is taken")
        return email

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if re.match("^\d{5}(?:[-\s]\d{4})?$", zip_code):
            if zip_code[2] in ['6', '7', '9']:
                return zip_code
            else:
                raise forms.ValidationError("The zip code provide do not belong to Puerto Rico")
        raise forms.ValidationError("Invalid zip code")

    def clean_phone(self):
        phone_number = self.cleaned_data.get('phone')
        if re.match("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$", phone_number):
            return phone_number
        raise forms.ValidationError("Invalid phone number")

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        confirmation_pass = self.cleaned_data.get('confirmation_pass')
        if password != confirmation_pass:
            raise forms.ValidationError("Passwords do not match")
        return data

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone', 'email']


class ProfileForm(RegisterForm):

    def __init__(self, request, *args, **kwargs):
        self.request = request
        location = kwargs['instance'].locations.last()
        kwargs.update(initial={'address': location.address,
                               'city': location.city,
                               'zip_code': location.zip_code})
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['username'].disabled = True
        self.fields['password'].required = False
        self.fields['password'].label = 'New password'
        self.fields['confirmation_pass'].required = False
        self.fields['confirmation_pass'].label = 'Confirm new password'
