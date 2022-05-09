from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Customer(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=50, default=' ')
    city = models.CharField(max_length=50, default=' ')
    state = models.CharField(max_length=50, default='')
    zipcode = models.CharField(max_length=10, default='00000')
    phone = models.CharField(max_length=20, default='(402)000-0000')
    email = models.EmailField(unique=False)


class Employee(models.Model):
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default='00000000')
    emp_id = models.IntegerField(blank=False, null=False, unique=True)
    emp_name = models.CharField(max_length=200)
    emp_email = models.EmailField(unique=False)
    emp_phone = models.CharField(max_length=20, default='(402)000-0000')

    def __str__(self):
        return 'Employee[username={},emp_id={},emp_name={}]'.format(
            self.username,
            self.emp_id,
            self.emp_name,
        )

# Create your models here.
