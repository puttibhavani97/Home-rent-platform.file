from django.contrib import admin
from .models import Property, Booking

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'price', 'bedrooms', 'rating']

class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'status', 'check_in_date', 'check_out_date', 'user_id', 'booking_date')

admin.site.register(Booking, BookingAdmin)
