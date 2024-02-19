from django.contrib import admin

from .models import City, Hotel


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    fields = ("name",)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    fields = ("name", "address", "phone", "city",)
