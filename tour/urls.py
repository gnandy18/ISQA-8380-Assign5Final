from django.urls import path

from tour.views import search_result

urlpatterns = [
    path('tours/', search_result, name='tour_list'),
]
