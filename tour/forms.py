
from functools import partial

import requests
from django import forms

from tour.models import TourPackage

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class Searchform(forms.Form):
    url = 'https://api.countrystatecity.in/v1/countries/us/cities'
    headers = {'Accept': 'application/json', 'X-CSCAPI-KEY': 'ZGdZTm42dXk1UlBtVlRxWVBITGhTb0k3QUMxUkxLWTNwM3BLZFhxTQ=='}
    res = requests.get(url, headers=headers).json()
    city_list = []
    city_list.append('')
    for r in res:
        value = r['name']
        if value not in city_list:
            city_list.append(value)

    leaving_from = forms.ChoiceField(choices=[(x, x) for x in city_list],
                                     widget=forms.Select(attrs={'class': 'filter__form__select'}))
    going_to = forms.ChoiceField(choices=[(x, x) for x in city_list],
                                 widget=forms.Select(attrs={'class': 'filter__form__select'}))
    tour_date = forms.DateField(widget=DateInput())
    no_days = forms.IntegerField()


class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = ('tour_number', 'tour_name', 'leaving_from', 'going_to', 'number_of_days', 'price', 'tour_date', 'description',)