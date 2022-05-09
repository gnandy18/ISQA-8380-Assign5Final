"""TourPackageBooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from tour import views
from tour.views import home_view, search_result, makeReservation

urlpatterns = [
    path('', home_view, name='home'),
    path('user/login', TemplateView.as_view(template_name='Registration/login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('tours/', search_result, name='tour_list'),
    path('tour_list', views.tour_list, name='tours_list'),
    path('tour/<int:pk>/edit/', views.tour_edit, name='tour_edit'),
    path('tour/<int:pk>/delete/', views.tour_delete, name='tour_delete'),
    path('tour/create/', views.tour_new, name='tour_new'),
    path('makeTourReservation/', makeReservation, name='make_reservation'),
    path('bookingList', views.viewBookings, name='view_bookings'),


]
