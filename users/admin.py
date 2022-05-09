from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Employee
from .forms import CustomUserCreationForm, CustomUserChangeForm, EmployeeForm


class CustomUserAdmin(UserAdmin):
    model = Customer
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'first_name', 'last_name', 'phone', ]


class EmployeeList(admin.ModelAdmin):
    model = Employee
    add_form = EmployeeForm
    list_display = ('emp_id', 'emp_name', 'emp_email', 'emp_phone')



admin.site.register(Employee, EmployeeList)

admin.site.register(Customer, CustomUserAdmin)
