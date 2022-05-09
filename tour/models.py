from django.db import models
from django.utils import timezone
from users.models import Customer


# Create your models here.


class Tour(models.Model):
    tour_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.tour_name)


class TourPackage(models.Model):
    tour_number = models.IntegerField(blank=False, null=False)
    tour_name = models.ForeignKey(Tour, on_delete=models.CASCADE)
    leaving_from = models.CharField(max_length=30)
    going_to = models.CharField(max_length=30)
    number_of_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tour_date = models.DateTimeField()
    description = models.CharField(max_length=1000)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.tour_number)


class Booking(models.Model):
    booking_id = models.AutoField(blank=False, null=False, primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)
    booking_total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    booking_date = models.DateTimeField(default=timezone.now)
    username = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.booking_id)


class BookingItem(models.Model):
    tour_id = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)