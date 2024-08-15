from django.contrib import admin
from .models import Hotel, Review, Booking

# Register your models here.

class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'rooms', 'ratings', 'address', 'phone']

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Review)
admin.site.register(Booking)