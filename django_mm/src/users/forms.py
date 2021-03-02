import re

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField(label='first name', max_length=20, required=True)
    last_name = forms.CharField(label='last name', max_length=20, required=True)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "placeholder": "email"
        }
    ))
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    confirmation_pass = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)
    phone = forms.CharField(label='Phone number', required=False)
    address = forms.CharField(label="Address", widget=forms.TextInput(), required=True)
    city = forms.CharField(label="City", max_length=15, required=True)
    zip_code = forms.CharField(label="Zip code", max_length=10, required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        queryset = User.objects.filter(username=username)
        if queryset.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        queryset = User.objects.filter(email=email)
        if queryset.exists():
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
