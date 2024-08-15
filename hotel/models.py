from django.db import models
from customer.models import Customer
# Create your models here.

class Hotel(models.Model):
    name = models.CharField(max_length=128)
    rooms = models.IntegerField()
    photo = models.ImageField(upload_to='hotel/media/images')
    ratings = models.DecimalField(max_digits=3, decimal_places=2)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=256)
    postcode = models.IntegerField()
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Review(models.Model):
    review = models.TextField(max_length=1024)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hotel

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='booking')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name