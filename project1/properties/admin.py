from django.contrib import admin
from .models import Property, Booking

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'price', 'bedrooms', 'rating']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'start_date', 'end_date', 'status')  # ✅ Correct fields
