from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm
from django.shortcuts import render


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'Registration/signup.html'

# Create your views here.
