from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Customer, Employee


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Customer
        fields = (
        'username', 'first_name', 'last_name', 'address', 'city', 'state', 'zipcode', 'phone', 'email')
        help_texts = {
            'username': 'Please use your username.',
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = (
        'username', 'first_name', 'last_name', 'address', 'city', 'state', 'zipcode', 'phone', 'email')


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('username', 'emp_id', 'emp_name', 'emp_email', 'emp_phone')
