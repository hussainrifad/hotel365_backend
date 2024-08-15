from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    age = models.IntegerField()
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='customer/media/images/', null=True, blank=True)
    birth_date = models.DateField()
    balance = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
