import datetime
import json
import ssl
import urllib
from urllib.request import urlopen

import requests
from amadeus import Client, ResponseError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils import timezone
from geopy import geocoders, Nominatim

from tour.forms import Searchform, TourPackageForm
from tour.models import TourPackage, Tour, Booking, BookingItem


@login_required
def home_view(request):
    if request.user.is_superuser:
        tours = TourPackage.objects.filter(created_date__lte=timezone.now())
        return render(request, 'TourBooking/all_tour_list.html',
                      {'tour_list': tours})
    else:
        sform = Searchform()
        return render(request, 'home.html', {'form': sform})


@login_required
def search_result(request):
    search_form = Searchform(request.POST)
    leaving_from = request.GET['leaving_from']
    going_to = request.GET['going_to']
    tour_date = request.GET['tour_date']
    no_days = request.GET['no_days']
    tour_list = TourPackage.objects.filter(leaving_from__iexact=leaving_from, going_to__iexact=going_to)

    convert_base_url = 'http://api.currencylayer.com/live?access_key='
    convert_api_key = '12e809555b4b89cd312aa4df691ec5d2'
    convert_currency = '&currencies=EUR'
    convert_format = '&format=1'
    convert_url = convert_base_url + convert_api_key + convert_currency + convert_format
    rates = requests.get(convert_url).json()
    eur_conv_rate = rates["quotes"]["USDEUR"]
    return render(request, 'TourBooking/tour_list.html', {'tlist': tour_list, 'eur_rate': eur_conv_rate})


def loadCurrentWeatherData(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=9d790e885dc3ce070745ae88a779772e'

    # converting JSON data to a dictionary
    city_weather = requests.get(url.format(city)).json()

    # data for variable list_of_data

    weather = {
        'city': city,
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'],
        'pressure': city_weather['main']['pressure'],
        'humidity': city_weather['main']['humidity'],
        'icon': city_weather['weather'][0]['icon']
    }

    return weather


def loadSafetyIndexData(city):
    amadeus = Client(
        client_id='up0cfjgrTbV0uu03DoGIsSeTs7O5NwR7',
        client_secret='OCXGFXmygBvduGYA',
        http=ssl_disabled_urlopen
    )

    try:
        geolocator = Nominatim(user_agent="travelsite")
        location = geolocator.geocode(city)
        response = amadeus.safety.safety_rated_locations.get(latitude=location.latitude, longitude=location.longitude,
                                                             radius=10)
        r = amadeus.duty_of_care.diseases.covid19_area_report.get(countryCode="US")
        print(response.data)
        print(r.data)
        print(r.data['areaAccessRestriction']['entry'])

    except ResponseError as err:
        print(err)

    pass


@login_required
def makeReservation(request):
    global total_prices, wdata
    selectedTours = request.POST.getlist('toursSelected')
    user = request.user
    tour_list = []
    booking = Booking(username=user)
    booking.save()
    booking_in = Booking.objects.get(booking_id=booking.booking_id)
    for t in selectedTours:
        tour = TourPackage.objects.get(pk=t)
        booking_items = BookingItem(booking_id=booking_in, tour_id=tour)
        booking_items.save()
        tour_list.append(tour)

    if tour_list.__len__() > 0:
        tour_list.sort(key=lambda r: r.tour_date)

        print(tour_list[0].tour_date)
        city = tour_list[0].going_to
        wdata = loadCurrentWeatherData(city)
        #safety = loadSafetyIndexData(city)

        total_prices = sum(t.price for t in tour_list)
        booking_in.booking_total_price = total_prices
        booking_in.save()
    return render(request, 'TourBooking/bookingInfo.html',
                  {'tour_list': tour_list, 'booking': booking.booking_id, 'total_price': total_prices,
                   'weather': wdata})


@login_required
def tour_list(request):
    tours = TourPackage.objects.filter(created_date__lte=timezone.now())
    return render(request, 'TourBooking/all_tour_list.html',
                  {'tour_list': tours})


@login_required
def tour_new(request):
    if request.method == "POST":
        form = TourPackageForm(request.POST)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.created_date = timezone.now()
            tour.save()
            tour = TourPackage.objects.filter(created_date__lte=timezone.now())
            return render(request, 'TourBooking/all_tour_list.html',
                          {'tour_list': tour})
    else:
        form = TourPackageForm()
    return render(request, 'TourBooking/tour_new.html', {'form': form})


@login_required
def tour_edit(request, pk):
    tour = get_object_or_404(TourPackage, pk=pk)
    if request.method == "POST":
        # update
        form = TourPackageForm(request.POST, instance=tour)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.updated_date = timezone.now()
            tour.save()
            tour = TourPackage.objects.filter(created_date__lte=timezone.now())
            return render(request, 'TourBooking/all_tour_list.html',
                          {'tour_list': tour})
    else:
        # edit
        form = TourPackageForm(instance=tour)
    return render(request, 'TourBooking/tour_edit.html', {'form': form})


@login_required
def tour_delete(request, pk):
    tour = get_object_or_404(TourPackage, pk=pk)
    tour.delete()
    return redirect('tours_list')


@login_required
def viewBookings(request):


    bookings = Booking.objects.filter(username=request.user)
    booking_items = []

    for booking in bookings:
        booking_item = BookingItem.objects.filter(booking_id=booking)
        for item in booking_item:
            booking_items.append(item)

    return render(request, 'TourBooking/viewBooking.html', {'bookings': bookings, 'booking_items': booking_items})


def ssl_disabled_urlopen(endpoint):
        context = ssl._create_unverified_context()
        return urlopen(endpoint, context=context)