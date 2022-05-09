from django.contrib import admin

# Register your models here.
# from .models import Customer
from .models import Tour, TourPackage, Booking


# class CustomerList(admin.ModelAdmin):
#     list_display = ('cust_number', 'name', 'city', 'cell_phone')
#     list_filter = ('cust_number', 'name', 'city')
#     search_fields = ('cust_number', 'name')
#     ordering = ['cust_number']


class TourList(admin.ModelAdmin):
    list_display = ('tour_number', 'name', 'city')
    list_filter = ('tour_number', 'name', 'city')
    search_fields = ('tour_number', 'name')
    ordering = ['tour_number']


admin.site.register(Tour)
admin.site.register(TourPackage)
admin.site.register(Booking)

